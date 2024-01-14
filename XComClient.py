import multiprocessing as mp
import asyncio
import json
import os
import websockets
from websockets.sync.client import connect
from websockets.server import serve


def task_processor(functions: dict, taskQueue: mp.Queue, returnMsgQ: mp.Queue, state):
    while True:
        try:
            if taskQueue.empty():
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
    def __init__(self):
        self.server = None
        self.functions = {}
        self.taskQ = mp.Queue()
        self.returnMsgQ = mp.Queue()
        self.clients = {}
        self.clientsCFG = {}
        self.blockbuffers = {}
        # interrupt
        self.manager = mp.Manager()
        state = self.manager.Value("i", 0)
        self.interrupt = state
        state.value = 0
        # functions
        self.taskProcessor = mp.Process(
            target=task_processor,
            args=(self.functions, self.taskQ, self.returnMsgQ, state),
            name="taskProcessor",
        )


    def asClient(self,ip):
        self.taskProcessor.start()
        asyncio.get_event_loop().run_until_complete(self.connect_cloud(ip))


    def asServer(self, ip, port):
        self.taskProcessor.start()
        local_server = serve(self.asServer_onRecv, ip, port)
        print("\033[93m Server started \033[0m")
        asyncio.get_event_loop().run_until_complete(local_server)
        asyncio.get_event_loop().create_task(self.global_send())
        asyncio.get_event_loop().run_forever()


    async def connect_cloud(self,ip):
        async with websockets.connect(ip) as websocket:
            print("\033[93m Connected to Server \033[0m")
            self.server_websocket = websocket
            receive_task = asyncio.create_task(self.asClient_onRecv(websocket))
            send_task = asyncio.create_task(self.global_send())
            await asyncio.gather(receive_task, send_task)


    async def asClient_onRecv(self, websocket):
        try:
            async for message in websocket:
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
                if taskId not in self.blockbuffers:
                    self.blockbuffers[taskId] = []
                if taskId not in self.clientsCFG:
                    self.clientsCFG[taskId] = {}
                taskContent = message[20:]

                await self.global_onRecv(-1, header, taskId, taskContent)

        except Exception as e:
            print(f"Error in websocket communication: {e}")


    async def asServer_onRecv(self, websocket):

        wsId = id(websocket)
        try:
            async for message in websocket:
                self.clients[wsId] = websocket

                await self.global_onRecv(wsId, message)

        except Exception as e:
            print(f"Error in websocket communication: {e}")

    async def global_onRecv(self, wsId, message):
        '''
        WebSocket Object should NOT go inside here, only wsID
        
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

        if wsId not in self.blockbuffers:
            self.blockbuffers[wsId] = []
        if wsId not in self.clientsCFG:
            self.clientsCFG[wsId] = {}

        content = message[20:]
        
        try:
            if header == "block":
                self.blockbuffers[wsId].append(content)
                return

            if header == "config":
                config_json = content
                config_data = json.loads(config_json)
                self.clientsCFG[wsId][header] = config_data
                self.returnMsgQ.put((wsId, header, taskId, "config received"))
                print(f"Config Data: {content}")
                return

            if header == "cancel":
                self.interrupt.value = 1
                print(f"Client {self.websocket} requested an interrupt.")
                return

            if wsId in self.blockbuffers:  # if there is a block buffer, concat it
                self.blockbuffers[wsId].append(content)
                content = b"".join(self.blockbuffers[wsId])
                del self.blockbuffers[wsId]  # clean buffer

            self.taskQ.put(
                (wsId, header, taskId, self.clientsCFG[wsId], content)
            )
            # await self.functions[header](self.clientsData[client_id],content)

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
                        await self.clientSend(result, header)
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

    def registerFunc(self, func):
        fun_name = func.__name__
        self.functions[fun_name] = func
