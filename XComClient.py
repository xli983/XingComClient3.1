import multiprocessing as mp
import asyncio
import json
import os
import websockets
from websockets.sync.client import connect
from websockets.server import serve




def task_processor(functions: dict,taskQueue: mp.Queue, returnMsgQ: mp.Queue, state):
    while True:
        try:
            if taskQueue.empty():
                continue
            task_tuple = taskQueue.get()
            client_id,header,task_id,client_data,content=task_tuple
            func = functions[header]

            if func:
                result=func(client_data, content)
            returnMsgQ.put((client_id,header,task_id,result))
        except Exception as e:
            print(f"Error in task processing: {e}")



        # task.byteBuffer += task.message[20:]
        # self.taskQueue.put((task.byteBuffer, task.config_data, task.client_id, "image2image"))
class ComClient:
    def __init__(self):
        self.server=None
        self.client=None
        self.functions = {
        }
        self.taskQueue = mp.Queue()
        self.returnMsgQ=mp.Queue()
        self.clients = {}
        self.clientsData = {}
        self.blockbuffers={}
        #interrupt
        self.manager = mp.Manager()
        state=self.manager.Value("i",0)
        self.interrupt=state
        state.value=0
        #functions
        self.taskProcessor =mp.Process(target=task_processor, args=(self.functions,self.taskQueue,self.returnMsgQ,state),name="taskProcessor")

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
        start_server = serve(self.asServer_onRecv,ip, port)
        print("\033[93m Server started \033[0m")
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().create_task(self.global_send())
        asyncio.get_event_loop().run_forever()


    async def asServer_onRecv(self,websocket):
        try:
            async for message in websocket:
                print("\033[93mheader:", message[:10].replace(b'\x00', b'').decode(),
                        "id:", message[10:20].decode(), "length:", len(message[20:]), "\033[0m")
                #connect client and save client id

                self.clients[id(websocket)] = websocket
                header=message[:10].replace(b'\x00', b'').decode()
                taskId=message[10:20]
                if id(websocket) not in self.blockbuffers:
                    self.blockbuffers[id(websocket)]=[]
                if id(websocket) not in self.clientsData:
                    self.clientsData[id(websocket)]={}
                taskContent=message[20:]
                
                await self.global_onRecv(id(websocket),header,taskId,taskContent)

        except Exception as e:
            print(f"Error in websocket communication: {e}")



    async def global_onRecv(self, client_id,header,task_Id,content):

        try:
            if header == "block":
                self.blockbuffers[client_id].append(content)
                return

            if header == "config":
                config_json =content
                config_data = json.loads(config_json)
                self.clientsData[client_id][header]=config_data
                self.returnMsgQ.put((client_id,header,task_Id,"config received"))
                print(f"Config Data: {content}")
                return

            if header == "cancel":
                self.interrupt.value=1
                print(f"Client {self.websocket} requested an interrupt.")
                return
            
            if client_id in self.blockbuffers:#if there is a block buffer, concat it
                self.blockbuffers[client_id].append(content)
                content=b"".join(self.blockbuffers[client_id])
                del self.blockbuffers[client_id]#clean buffer

            self.taskQueue.put((client_id,header,task_Id,self.clientsData[client_id],content))
            #await self.functions[header](self.clientsData[client_id],content)

        except Exception as e:
            print(f"Error in websocket communication: {e}")
            return
    
     
    async def global_send(self):
        while True:
            if self.returnMsgQ.empty():
                await asyncio.sleep(0.1)
            else:
                try:
                    result_tuple = self.returnMsgQ.get()
                    client_id,header,task_id,content = result_tuple
                    header = (header+"0"*(10-len(header))).encode('utf-8')
                    if isinstance(task_id, str):
                        task_id = task_id.encode('utf-8')
                    if isinstance(header, str):
                        header = header.encode('utf-8')
                    if isinstance(content, str):
                        content = content.encode('utf-8')
                    if client_id == -1:
                        await self.clientSend(result,header)
                    else:
                        await self.asServer_send(client_id,header,task_id,content)
                except Exception as e:
                    print(f"Error in sending message to websocket: {e}")
    
    async def asServer_send(self,client_id,header,task_id,content):
        websocket = self.clients.get(client_id)
        while len(content)>0:
            if len(content)>100000:
                await websocket.send(b"block00000"+task_id+content[0:100000])
                content=content[100000:]
            else:
                await websocket.send(header+task_id+content)
                content = b""
            await asyncio.sleep(0.01)
        await asyncio.sleep(0.01)

    def registerFunc(self, func):
        fun_name=func.__name__
        self.functions[fun_name]=func






