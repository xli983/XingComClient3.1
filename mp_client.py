import multiprocessing as mp
import asyncio
import json
import os
import main
import websockets
from websockets.sync.client import connect
from task_processor import image_processor
from main import cleanup_temp
import cuda_malloc
from comfy.cli_args import args
from task_processor import image_processor, CrossProcess

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

init()

class Client:
    def __init__(self):
        self.server_uri = "wss://xing.art/com" 
        self.clientIdList = {}
        self.task_queue = mp.Queue()
        self.task_id = None
        self.sendingMessage_queue = mp.Queue()
        self.positionInqueue = []
        self.byteBuffer = b""
        self.config_data = None 
        #interrupt
        self.manager = mp.Manager()
        state=self.manager.Value("i",0)
        CrossProcess.interrupt=state
        state.value=0
        self.currentProgressObject = self.manager.dict()
        self.processor = mp.Process(target=image_processor, args=(self.task_queue, self.sendingMessage_queue,state))

    async def receive_from_server(self, websocket):
        try:
            async for message in websocket:
                # Config
                if message[0:6] == b"config":
                    config_json = message[20:].decode()
                    self.config_data = json.loads(config_json)
                    print(f"Config Data: {self.config_data}")
                    await websocket.send(message[10:20] + b"successReceiveConfig")
                # Image block
                elif message[0:5] == b"block":
                    print(message)
                    self.byteBuffer += message[20:]
                # Last image block
                elif message[0:3] == b"i2i":
                    print(f"Received final image block, length: {len(message)}")
                    self.task_id = message[10:20]
                    self.byteBuffer += message[20:]
                    self.task_queue.put((self.byteBuffer, self.config_data, self.task_id))
                    self.byteBuffer = b""  # Clean buffer
        except Exception as e:
            print(f"Error in websocket communication: {e}")

    async def process_results(self, websocket):
        while True:
            if self.sendingMessage_queue.empty():
                await asyncio.sleep(0.1)
            else:
                try:
                    result_tuple = self.sendingMessage_queue.get()
                    content, task_id, Messagetype = result_tuple
                    if Messagetype == "image":
                        while len(content)>0:
                            if len(content)>100000:
                                await websocket.send(b"block00000"+task_id+content[0:100000])
                                content=content[100000:]
                            else:
                                await websocket.send(b"i2i0000000"+task_id+content)
                                content = b""
                            await asyncio.sleep(0.01)
                    if Messagetype == "id":
                        await websocket.send(b"0000000000" + content)
                except Exception as e:
                    print(f"Error in sending message to websocket: {e}")

    async def start(self):
        main.cleanup_temp()
        self.processor.start()
        async with websockets.connect(self.server_uri) as websocket:
            receive_task = asyncio.create_task(self.receive_from_server(websocket))
            send_task = asyncio.create_task(self.process_results(websocket))
            await asyncio.gather(receive_task, send_task)

if __name__ == '__main__':
    cleanup_temp()
    client = Client()
    asyncio.get_event_loop().run_until_complete(client.start())
