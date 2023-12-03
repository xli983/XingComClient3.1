#----------------------------------------------Initialization---------------------------------------------------------
import multiprocessing as mp
import asyncio
import json
import main
from websockets.server import serve
from task_processor import i2i_processor, CrossProcess, i2t_processor
from comfy.cli_args import args


class Server:
    def __init__(self):
        # self.initial()
        self.clientIdList = {}
        self.i2iQueue= mp.Queue()
        self.i2tQueue= mp.Queue()
        self.sendingMessage_queue = mp.Queue()
        self.positionInqueue = []

        self.functions = {
            'config': self.config,
            'block': self.block,
            'i2i': self.i2i,
            'cancel': self.cancel,
            'i2t': self.i2t
        }

        #interrupt
        self.manager = mp.Manager()
        state=self.manager.Value("i",0)
        CrossProcess.interrupt=state
        state.value=0

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
        if self.mode != 'i2i':
            self.switch = True
            self.target_mode = 'i2i'
            await self.tryswitch()
        
        print(f"{self.websocket} received final buffer block, length: {len(self.message)}")
        setattr(self.websocket, 'task_id', self.task_id)
        self.byteBuffer += self.message[20:]
        self.positionInqueue.append(id(self.websocket))
        self.i2iQueue.put((self.byteBuffer, self.config_data, id(self.websocket)))
        self.byteBuffer = b"" # clean buffer
    
    async def i2t(self):
        if self.mode != 'i2t':
            self.switch = True
            self.target_mode = 'i2t'
            await self.tryswitch()
        
        setattr(self.websocket, 'task_id', self.task_id)
        self.byteBuffer += self.message[20:]
        self.positionInqueue.append(id(self.websocket))
        self.i2tQueue.put((self.byteBuffer, id(self.websocket)))
        self.byteBuffer = b"" # clean buffer

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

                func = self.functions.get(header)
                if func:
                    await func()

        except Exception as e:
            print(f"Error in websocket communication: {e}")


    async def process_results(self):
        while True:
            if self.sendingMessage_queue.empty():
                await asyncio.sleep(0.1)  # Sleep for a bit if the queue is empty
            else:
                try:
                    if self.switch:
                        await self.tryswitch()
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
                    if Messagetype == "prompt":
                        first_client_id = self.positionInqueue.pop(0)
                        for i, client_id in enumerate(self.positionInqueue):
                            otherWebsocket = self.clientIdList.get(client_id)
                            if i != 0:
                                await otherWebsocket.send(f"position: {i}")
                        await websocket.send({content})
                    if Messagetype == "message":
                        await websocket.send({content})
                    if Messagetype == "id":
                        await websocket.send(b"0000000000" + content)
                except Exception as e:
                    print(f"Error in sending message to websocket: {e}")

            
    def start(self):
        self.processor.start()
        start_server = serve(self.handle_client, "143.215.97.158", 8765)
        print("server open")
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().create_task(self.process_results())
        asyncio.get_event_loop().run_forever()

if __name__ == '__main__':
    server = Server()
    server.start()
