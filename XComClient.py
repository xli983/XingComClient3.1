import multiprocessing as mp
import asyncio
import json
import os
import websockets
from websockets.sync.client import connect
from websockets.server import serve
import time

import sys
class ConsoleCapture:
    def __init__(self):
        self.output = ["" for _ in range(10)] # Capture the last 10 lines

    def write(self, text):
        # Capture the printed text
        if(text == '\n'):
            return
        self.output.append(text)
        self.output.pop(0)

        sys.stdout= sys.__stdout__
        print(text)
        sys.stdout = self

    def flush(self):
        pass
    
# Redirect sys.stdout to the custom stream
capture_stream = ConsoleCapture()
sys.stdout = capture_stream

def process_process(functions: dict, taskQueue: mp.Queue, returnMsgQ: mp.Queue):
    while True:
        try:
            if taskQueue.empty():
                time.sleep(0.1)
                continue
            task_tuple = taskQueue.get()
            client_id, header, task_id, client_data, content = task_tuple
            func = functions[header]

            if func:
                result = func(client_data, content)
            returnMsgQ.put((client_id, header, task_id, result))


        except Exception as e:
            print(f"Error in task processing: {e}")


class ComClient:
    def __init__(self,funcs,mode: str, ip=None, port=None):
        '''
        init a ComClient with AI functions
        funcs: a list of AI functions
        '''
        self.server = None
        self.registered_funcs = {}

        for f in funcs:
            fun_name = f.__name__
            self.registered_funcs[fun_name] = f

        self.taskQ = mp.Queue()
        self.returnMsgQ = mp.Queue()
        self.clients = {}
        self.clientsCFG = {}
        self.blockbuffers = {}
        self.manager = mp.Manager()

        # functions
        self.taskProcessor = mp.Process(
            target=process_process,
            args=(self.registered_funcs, self.taskQ, self.returnMsgQ),
            name="taskProcessor",
        )


        if(mode == "server"):
            print("\033[93m Server started \033[0m")
            asyncio.get_event_loop().run_until_complete(serve(self.asServer_onRecv, ip, port))
        elif(mode == "client"):
            asyncio.get_event_loop().create_task(self.connect_cloud(ip))

        self.taskProcessor.start()
        
        asyncio.get_event_loop().create_task(self.global_send())
        asyncio.get_event_loop().run_forever()




    async def connect_cloud(self,ip):
        async with websockets.connect(ip) as websocket:
            print("\033[93m===========         Connected to the server         ============\033[0m")
            print("\033[93m===========         Connected to the server         ============\033[0m")
            print("\033[93m===========         Connected to the server         ============\033[0m")
            self.server_websocket = websocket
            try:
                while True:
                    message = await websocket.recv()
                    ###### -1 should be client id, change it later
                    await self.global_onRecv(-1, message)
            except websockets.ConnectionClosedError:
                print("Connection closed by the server")


    async def asServer_onRecv(self, websocket):

        clientID = id(websocket)
        print(f"Client {clientID} connected")
        try:
            async for message in websocket:
                self.clients[clientID] = websocket

                await self.global_onRecv(clientID, message)

        except Exception as e:
            print(f"Error in websocket communication: {e}")

    async def global_onRecv(self, clientID, message):
        '''
        WebSocket Object should NOT go inside here, only clientID and message
        
        '''
        print(
            "\033[93mheader:",
            message[:10].replace(b"\x00", b"").decode(),
            "id:",
            message[10:20].decode(),
            "length:",
            len(message[20:]),
            "\033[0m",
        )
        # connect client and save client id

        header = message[:10].replace(b"\x00", b"").decode()
        taskId = message[10:20]

        if clientID not in self.blockbuffers:
            self.blockbuffers[clientID] = []
        if clientID not in self.clientsCFG:
            self.clientsCFG[clientID] = {}

        content = message[20:]
        
        try:
            if header == "block":
                # if block, save it to buffer
                self.blockbuffers[clientID].append(content)
                return

            if header == "config":
                # if config, save it to config
                config_json = content
                config_data = json.loads(config_json)
                self.clientsCFG[clientID][header] = config_data
                self.returnMsgQ.put((clientID, header, taskId, "config received"))
                print(f"Config Data: {content}")
                return

            if header == "cancel":
                # if cancel, cancel the task, not implemented yet
                raise NotImplementedError
                self.interrupt.value = 1
                print(f"Client {self.websocket} requested an interrupt.")
                return
            

            #if program reaches here, it means it is a normal task


            if clientID in self.blockbuffers:
                # if there is a block buffer, concat it
                self.blockbuffers[clientID].append(content)
                content = b"".join(self.blockbuffers[clientID])
                del self.blockbuffers[clientID] # clean buffer

            self.taskQ.put(
                (clientID, header, taskId, self.clientsCFG[clientID], content)
            )

        except Exception as e:
            print(f"Error in websocket communication: {e}")
            return

    async def asClient_send(self, header, task_id, content):
        while len(content) > 0:
            if len(content) > 100000:
                await self.server_websocket.send(
                    b"block00000" + task_id + content[0:100000]
                )
                content = content[100000:]
            else:
                await self.server_websocket.send(header + task_id + content)
                content = b""
            await asyncio.sleep(0.01)
        await asyncio.sleep(0.01)

    async def global_send(self):
        while True:
            if self.returnMsgQ.empty():
                await asyncio.sleep(0.1)
            else:
                try:
                    result_tuple = self.returnMsgQ.get()
                    client_id, header, task_id, content = result_tuple
                    header = (header + "0" * (10 - len(header))).encode("utf-8")
                    if isinstance(task_id, str):
                        task_id = task_id.encode("utf-8")
                    if isinstance(header, str):
                        header = header.encode("utf-8")
                    if isinstance(content, str):
                        content = content.encode("utf-8")
                    if client_id == -1:
                        await self.server_websocket.send(header + task_id + content)
                    else:
                        await self.asServer_send(client_id, header, task_id, content)
                except Exception as e:
                    print(f"Error in sending message to websocket: {e}")

    async def asServer_send(self, client_id, header, task_id, content):
        websocket = self.clients.get(client_id)
        while len(content) > 0:
            if len(content) > 100000:
                await websocket.send(b"block00000" + task_id + content[0:100000])
                content = content[100000:]
            else:
                await websocket.send(header + task_id + content)
                content = b""
            await asyncio.sleep(0.01)
        await asyncio.sleep(0.01)


