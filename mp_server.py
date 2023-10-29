#----------------------------------------------Initialization---------------------------------------------------------
import multiprocessing as mp
import asyncio
import json
import os
import main
from websockets.server import serve
from task_processor import image_processor, CrossProcess
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
        self.functions = [self.config, self.block, self.i2i, self.cancel]
        #interrupt
        self.manager = mp.Manager()
        state=self.manager.Value("i",0)
        CrossProcess.interrupt=state
        state.value=0
        self.currentProgressObject = self.manager.dict()
        self.processor = mp.Process(target=image_processor, args=(self.task_queue, self.sendingMessage_queue,state))

    async def connect(self):
        self.clientIdList[id(self.websocket)] = self.websocket
        setattr(self.websocket, 'client_id', id(self.websocket))

    async def config(self):
        task = getattr(self.websocket, 'task', None)
        if task is not None:
            print("Client already has a processing request pending. Blocking new request.")
            return
        self.sendingMessage_queue.put((self.message[:20],id(self.websocket),"message"))
        config_json =self.message[20:].decode()
        self.config_data = json.loads(config_json)
        print(f"Config Data: {self.config_data}")
    
    async def block(self):
        self.byteBuffer += self.message[20:]


    async def i2i(self):
        print(f"{self.websocket} received final buffer block, length: {len(self.message)}")
        setattr(self.websocket, 'task_id', self.task_id)
        self.byteBuffer += self.message[20:]
        self.positionInqueue.append(id(self.websocket))
        #if len(self.positionInqueue) != 1:
            #await websocket.send(f"position: {len(self.positionInqueue)-1}")
        self.task_queue.put((self.byteBuffer, self.config_data, id(self.websocket)))
        self.byteBuffer = b"" # clean buffer

    async def cancel(self):
        CrossProcess.interrupt.value=1
        print(f"Client {self.websocket} requested an interrupt.")

    async def handle_client(self, websocket, path):
        self.byteBuffer = b""
        self.config_data = None 
        try:
            async for message in websocket: #save client id and task id
                self.message = message
                self.websocket = websocket
                header = message[:10].decode('utf-8').rstrip('\x00')
                self.task_id = message[10:20]
                print("received " + str(header)+str(self.task_id)) 

                client_id = getattr(websocket, 'client_id', None)
                if client_id is None:
                    client_id = id(websocket)
                    await self.connect()

                for i in range(0,len(self.functions)):
                    if(header==self.functions[i].__name__):
                        await self.functions[i]()
                

                #config
                # if message[0:6]==b"config":
                #     task = getattr(websocket, 'task', None)
                #     if task is not None:
                #         print("Client already has a processing request pending. Blocking new request.")
                #         continue
                #     config_json = message[20:].decode()
                #     config_data = json.loads(config_json)
                #     print(f"Config Data: {config_data}")
                #     continue

                #image block
                # if message[0:8]==b"imgblock":#imgblock
                #     byteBuffer += message[20:]
                #     continue
                #last image block
                #if message[0:8]==b"endblock":
                    # print(f"{websocket} received final buffer block, length: {len(message)}")
                    # byteBuffer += message[20:]
                    # current_client_id = getattr(websocket, 'client_id', None)
                    # self.positionInqueue.append(current_client_id)
                    # if len(self.positionInqueue) != 1:
                    #     await websocket.send(f"position: {len(self.positionInqueue)-1}")
                    # setattr(websocket, 'com_id', message[10:20])
                    # self.task_queue.put((byteBuffer, config_data, current_client_id))
                    # byteBuffer = b"" # clean buffer
                #cancel
                # if message[0:6] == b"cancel":
                #     CrossProcess.interrupt.value=1
                #     print(f"Client {websocket} requested an interrupt.")
                #     continue
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
                    task_id = getattr(websocket, 'task_id', None)
                    if Messagetype == "image":
                        first_client_id = self.positionInqueue.pop(0)
                        for i, client_id in enumerate(self.positionInqueue):
                            otherWebsocket = self.clientIdList.get(client_id)
                            if i != 0:
                                await otherWebsocket.send(f"position: {i}")
                        print(len(content))
                        while len(content)>0:
                            if len(content)>100000:
                                await websocket.send(b"block00000"+task_id+content[0:100000])
                                content=content[100000:]
                            else:
                                await websocket.send(b"i2i0000000"+task_id+content)
                                content = b""
                            await asyncio.sleep(0.01)
                        await asyncio.sleep(0.01)
                    # if Messagetype == "position":
                    #     await websocket.send(f"position: {content}")
                    if Messagetype == "message":
                        await websocket.send({content})
                    # if Messagetype == "progress":
                    #     await websocket.send(f"progress:{content}")
                    if Messagetype == "id":
                        await websocket.send(b"0000000000" + content)
                except Exception as e:
                    print(f"Error in sending message to websocket: {e}")

            
    def start(self):
        main.cleanup_temp()
    
        self.processor.start()
        start_server = serve(self.handle_client, "143.215.111.114", 8765)
        print("server open")
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().create_task(self.process_results())
        asyncio.get_event_loop().run_forever()

if __name__ == '__main__':
    init()
    cleanup_temp()
    server = Server()
    server.start()
