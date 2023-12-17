import multiprocessing as mp
import asyncio
import json
import os
import main
import websockets
from websockets.sync.client import connect
from websockets.server import serve
from main import cleanup_temp
from XComClient_Processor import task_processor,CrossProcess, image2image, image2text



class Task:
    def __init__(self, client_id, message):
        self.message = message
        self.client_id = client_id
        self.task_id =  message[10:20]
        self.byteBuffer = b""
        self.config_data = None
        self.type = None


class ComClient:
    def __init__(self):
        self.server=None
        self.client=None
        self.functions = {
            'config': self.config,
            'block': self.block,
            'i2i': self.i2i,
            'cancel': self.cancel,
            'i2t': self.i2t
        }
        self.taskQueue = mp.Queue()
        self.returnMsgQ=mp.Queue()
        self.clientIdList = {}
        self.functionDic = {}
        #interrupt
        self.manager = mp.Manager()
        state=self.manager.Value("i",0)
        CrossProcess.interrupt=state
        state.value=0
        #functions
        self.taskProcessor =mp.Process(target=task_processor, args=(self.functionDic,self.taskQueue,self.returnMsgQ,state))

    def asClient():
        return

        # def websocketrec():
        #     async for message in websocket:
        #         self.onRecv(msg)
        #         pass
        # def process_results():
        #     while True:
        #         #get msg from returnMsgQ
        #         #if have no clientId, return it
        #         pass
        # async with websockets.connect(self.server_uri) as websocket:
        #     receive_task = asyncio.create_task(websocketrec(websocket))
        #     send_task = asyncio.create_task(self.process_results(websocket))
        #     await asyncio.gather(receive_task, send_task)
            
    def asServer(self,ip, port):
        self.taskProcessor.start()
        start_server = serve(self.handle_client,ip, port)
        print("server open")
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().create_task(self.process_results())
        asyncio.get_event_loop().run_forever()

    async def handle_client(self,websocket):
        try:
            async for message in websocket:
                print(message)
                #connect client and save client id
                client_id = getattr(websocket, 'client_id', None)
                if client_id is None:
                    client_id = id(websocket)
                    await self.connect(websocket)
                setattr(websocket, 'task_id', message[10:20]) 
                taskObject = getattr(websocket, 'task', None)
                if taskObject is None:
                    taskObject = Task(client_id,message)
                    setattr(websocket, 'task', taskObject)
                taskObject.message = message
                func = self.functions.get(message[:10].decode('utf-8').rstrip('\x00'))
                if func:
                    await func(taskObject)
        except Exception as e:
            print(f"Error in websocket communication: {e}")


    async def connect(self,websocket):
        self.clientIdList[id(websocket)] = websocket
        setattr(websocket, 'client_id', id(websocket))


    async def onRecv(self, client_id, message):
        taskObject = Task(client_id,message)
        func = self.functions.get(taskObject.header)
        if func:
            await func(taskObject)
        return 
    #-------------------------------------Com Functions Start here--------------------------------------------#
    async def config(self,task):
        config_json =task.message[20:].decode()
        task.config_data = json.loads(config_json)
        self.returnMsgQ.put((task.message[:20],task.client_id,"message"))
        print(f"Config Data: {task.config_data}")
    
    async def block(self,task):
        task.byteBuffer += task.message[20:]

    async def i2i(self,task):      
        task.byteBuffer += task.message[20:]
        self.taskQueue.put((task.byteBuffer, task.config_data, task.client_id, "image2image"))
        task.byteBuffer = b"" # clean buffer
    
    async def i2t(self,task):
        task.byteBuffer += task.message[20:]
        self.taskQueue.put((task.byteBuffer, task.config_data, task.client_id, "image2text"))
        task.byteBuffer = b"" # clean buffer

    async def cancel(self,task):
        CrossProcess.interrupt.value=1
        print(f"Client {self.websocket} requested an interrupt.")
    
    #--------------------------------------------------Com Functions end here ------------------------------------
     
    async def process_results(self):
        while True:
            if self.returnMsgQ.empty():
                await asyncio.sleep(0.1)
            else:
                try:
                    result_tuple = self.returnMsgQ.get()
                    result,client_id,task_type = result_tuple
                    if client_id == -1:
                        await self.clientSend(result,task_type)
                    else:
                        await self.serverSend(result,client_id,task_type)
                except Exception as e:
                    print(f"Error in sending message to websocket: {e}")
    
    async def serverSend(self,result,client_id,task_type):
        websocket = self.clientIdList.get(client_id)
        task_id = getattr(websocket, 'task_id', None)
        if task_type == "message":
            await websocket.send({result})
        if task_type == "image2image":
            # first_client_id = self.positionInqueue.pop(0)
            # for i, client_id in enumerate(self.positionInqueue):
            #     otherWebsocket = self.clientIdList.get(client_id)
            #     if i != 0:
            #         await otherWebsocket.send(f"position: {i}")
            if result == "Canceled":
                await websocket.send({result})
            while len(result)>0:
                if len(result)>100000:
                    await websocket.send(b"block00000"+task_id+result[0:100000])
                    result=result[100000:]
                else:
                    await websocket.send(b"i2i0000000"+task_id+result)
                    result = b""
                await asyncio.sleep(0.01)
            await asyncio.sleep(0.01)
        if task_id == "task_type":
            # first_client_id = self.positionInqueue.pop(0)
            # for i, client_id in enumerate(self.positionInqueue):
            #     otherWebsocket = self.clientIdList.get(client_id)
            #     if i != 0:
            #         await otherWebsocket.send(f"position: {i}")
            await websocket.send({result})

    def registerFunc(self, func):
        if func == "image2image":
            self.functionDic[func] = image2image
        if func == "image2text":
            self.functionDic[func] = image2text






