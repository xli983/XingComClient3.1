import multiprocessing as mp
import asyncio
import json
import os
import main
import websockets
from websockets.sync.client import connect
from main import cleanup_temp
from task_processor import i2i_processor, i2t_processor, CrossProcess


class Client:
    def __init__(self):
        self.server_uri = "wss://xing.art/com" 
        self.clientIdList = {}
        self.i2iQueue = mp.Queue()
        self.i2tQueue = mp.Queue()
        self.task_id = None
        self.sendingMessage_queue = mp.Queue()
        self.positionInqueue = []
        self.functions = {
            'config': self.config,
            'block': self.block,
            'i2i': self.i2i,
            'cancel': self.cancel,
            'i2t': self.i2t
        }
        self.byteBuffer = b""
        self.config_data = None 
        #interrupt
        self.manager = mp.Manager()
        state=self.manager.Value("i",0)
        CrossProcess.interrupt=state
        state.value=0

        #mode
        self.mode = 'i2i'
        self.target_mode = 'i2i'
        self.switch = False

        self.currentProgressObject = self.manager.dict()
        self.processor = mp.Process(target=i2i_processor, args=(self.i2iQueue, self.sendingMessage_queue,state))
    
    def switch_processor(self):
        if self.processor is not None and self.processor.is_alive():
            self.processor.terminate()
            self.processor.join() 
        state = CrossProcess.interrupt
        if self.mode == 'i2i':
            self.processor = mp.Process(target=i2i_processor, args=(self.i2iQueue, self.sendingMessage_queue,state))
        elif self.mode == 'i2t':
            self.processor = mp.Process(target=i2t_processor, args=(self.i2tQueue, self.sendingMessage_queue, state))
        self.processor.start()
        self.switch = False
        print("Processor has been switched to"+ self.mode)

    async def config(self):
        config_json = self.message[20:].decode()
        self.config_data = json.loads(config_json)
        print(f"Config Data: {self.config_data}")
    
    async def block(self):
        self.byteBuffer += self.message[20:]

    async def i2i(self):
        if self.mode != 'i2i':
            self.switch = True
            self.target_mode = 'i2i'
            await self.tryswitch()
        print(f"Received final image block, length: {len(self.message)}")
        self.task_id = self.message[10:20]
        self.byteBuffer += self.message[20:]
        self.i2iQueue.put((self.byteBuffer, self.config_data, self.task_id))
        self.byteBuffer = b""  # Clean buffer

    async def i2t(self):
        if self.mode != 'i2t':
            self.switch = True
            self.target_mode = 'i2t'
            await self.tryswitch()
        self.task_id = self.message[10:20]
        self.byteBuffer += self.message[20:]
        self.i2tQueue.put((self.byteBuffer, self.config_data, self.task_id))
        self.byteBuffer = b""  # Clean buffer

    async def cancel(self):
        CrossProcess.interrupt.value=1
        print(f"Client {self.websocket} requested an interrupt.")

    async def tryswitch(self):
        if (self.mode == 'i2i') & self.i2iQueue.empty():
            self.mode = self.target_mode
            self.switch_processor()
        if (self.mode == 'i2t') & self.i2tQueue.empty():
            self.mode = self.target_mode
            self.switch_processor()
        

    async def receive_from_server(self, websocket):
        try:
            async for message in websocket:
                self.message = message
                header = message[:10].decode('utf-8').rstrip('\x00')
                self.task_id = message[10:20]
                print("received " + str(header)+str(self.task_id)) 
                func = self.functions.get(header)
                if func:
                    await func()
        except Exception as e:
            print(f"Error in websocket communication: {e}")
            raise e

    async def process_results(self, websocket):
        while True:
            if self.sendingMessage_queue.empty():
                await asyncio.sleep(0.1)
            else:
                try:
                    if self.switch:
                        await self.tryswitch()
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
                    if Messagetype == "prompt":
                        first_client_id = self.positionInqueue.pop(0)
                        for i, client_id in enumerate(self.positionInqueue):
                            otherWebsocket = self.clientIdList.get(client_id)
                            if i != 0:
                                await otherWebsocket.send(f"position: {i}")
                        await websocket.send({content})
                    if Messagetype == "id":
                        await websocket.send(b"0000000000" + content)
                except Exception as e:
                    print(f"Error in sending message to websocket: {e}")
                    raise e

    async def start(self):
        self.processor.start()
        async with websockets.connect(self.server_uri) as websocket:
            receive_task = asyncio.create_task(self.receive_from_server(websocket))
            send_task = asyncio.create_task(self.process_results(websocket))
            await asyncio.gather(receive_task, send_task)

def main_program():
    client = Client()
    asyncio.get_event_loop().run_until_complete(client.start())

if __name__ == '__main__':
    while True:
        try:
            main_program()
        except Exception as e:
            print(f"Error encountered: {e}. Restarting the program...")
            continue


