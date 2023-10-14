#----------------------------------------------Initialization---------------------------------------------------------
import multiprocessing as mp
import asyncio
import json
import os
import main
from websockets.server import serve
from task_processor import image_processor
from main import cleanup_temp
import cuda_malloc
from comfy.cli_args import args

def init():
    main.execute_prestartup_script()
    if os.name == "nt":
        import logging
        logging.getLogger("xformers").addFilter(lambda record: 'A matching Triton is not available' not in record.getMessage())

    if __name__ == "__main__":
        if args.cuda_device is not None:
            os.environ['CUDA_VISIBLE_DEVICES'] = str(args.cuda_device)
            print("Set cuda device to:", args.cuda_device)
    image = None

class Server:
    def __init__(self):
        # self.initial()
        self.clientIdList = {}
        self.task_queue = mp.Queue()
        self.sendingMessage_queue = mp.Queue()
        self.positionInqueue = []
        self.processor = mp.Process(target=image_processor, args=(self.task_queue, self.sendingMessage_queue))

    async def handle_client(self, websocket, path):
        byteBuffer = b""
        config_data = None 
        interrupt_processing = False
        interrupt_processing_mutex = mp.Lock()
        try:
            async for message in websocket:
                current_client_id = getattr(websocket, 'client_id', None)
                if current_client_id is None:
                    current_client_id = id(websocket)
                    self.clientIdList[current_client_id] = websocket
                    setattr(websocket, 'client_id', current_client_id)
                #config
                if message[0:6]==b"config":
                    task = getattr(websocket, 'task', None)
                    if task is not None:
                        print("Client already has a processing request pending. Blocking new request.")
                        continue
                    config_json = message[20:].decode()
                    config_data = json.loads(config_json)
                    print(f"Config Data: {config_data}")
                    self.sendingMessage_queue.put((message[10:20]+b"successReceiveConfig",current_client_id,'id'))
                    continue
                #image block
                if message[0:8]==b"imgblock":#imgblock
                    byteBuffer += message[20:]
                    continue
                #last image block
                if message[0:8]==b"endblock":
                    print(f"{websocket} received final buffer block, length: {len(message)}")
                    byteBuffer += message[20:]
                    current_client_id = getattr(websocket, 'client_id', None)
                    self.positionInqueue.append(current_client_id)
                    if len(self.positionInqueue) != 1:
                        await websocket.send(f"position: {len(self.positionInqueue)-1}")
                    setattr(websocket, 'com_id', message[10:20])
                    self.task_queue.put((byteBuffer, config_data, current_client_id))
                    byteBuffer = b"" # clean buffer
                #cancel
                if message == "cancel":
                    with interrupt_processing_mutex:
                        interrupt_processing = True
                    print(f"Client {websocket} requested an interrupt.")
                    continue
        except Exception as e:
            print(f"Error in websocket communication: {e}")


    async def process_results(self):
        while True:
            if self.sendingMessage_queue.empty():
                await asyncio.sleep(0.1)  # Sleep for a bit if the queue is empty
            else:
                try:
                    result_tuple = self.sendingMessage_queue.get()
                    content, client_id, Messagetype = result_tuple
                    websocket = self.clientIdList.get(client_id)
                    com_id = getattr(websocket, 'com_id', None)
                    if Messagetype == "image":
                        first_client_id = self.positionInqueue.pop(0)
                        for i, client_id in enumerate(self.positionInqueue):
                            otherWebsocket = self.clientIdList.get(client_id)
                            if i != 0:
                                await otherWebsocket.send(f"position: {i}")
                        print(len(content))
                        while len(content)>0:
                            if len(content)>100000:
                                await websocket.send(b"block00000"+b"0000000000"+content[0:100000])
                                content=content[100000:]
                            else:
                                await websocket.send(b"endblock00"+com_id+content)
                                content = b""
                            await asyncio.sleep(0.01)
                        await asyncio.sleep(0.01)
                    # if Messagetype == "position":
                    #     await websocket.send(f"position: {content}")
                    # if Messagetype == "message":
                    #     await websocket.send(f"update: {content}")
                    # if Messagetype == "progress":
                    #     await websocket.send(f"progress:{content}")
                    if Messagetype == "id":
                        await websocket.send(b"0000000000" + content)
                except Exception as e:
                    print(f"Error in sending message to websocket: {e}")

            
    def start(self):
        main.cleanup_temp()
    
        self.processor.start()
        start_server = serve(self.handle_client, "143.215.106.165", 8765)
        print("server open")
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().create_task(self.process_results())
        asyncio.get_event_loop().run_forever()

if __name__ == '__main__':
    init()
    cleanup_temp()
    server = Server()
    server.start()
