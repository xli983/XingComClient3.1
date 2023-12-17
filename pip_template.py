# class AsServer:
#     def __init__(self) -> None:
#         #start server
#         pass

#     def onRecv():
#         #add msg to msgQ
#         #msgQ.push([clientId,taskId,header.....])
#         return 
    
#     def send():
#         while True:
#             #get msg from returnMsgQ
#             #if have clientId, return it

# class AsClient:
#     def __init__(self) -> None:
#         #connnet to xing server
#         pass
    
#     def onRecv():
#         #add msg to msgQ
#         #msgQ.push([-1,taskId,header.....])
#         return 
    
#     def send():
#         while True:
#             #get msg from returnMsgQ
#             #if have no clientId, return it

class ComClient:
    def __init__(self) -> None:
        self.server=None
        self.client=None

    def asClient():
        #connet ot xing server
        self.client=.......
        async for message in websocket:
            #onRecv(msg)
    def asServer():
        self.server=.......
        try:
            async for message in websocket: #save client id and task id
                #onRecv(msg)
        except Exception as e:
            print(f"Error in websocket communication: {e}")
        #start local ws server

    def onRecv(msg):
        #receive msg from both server and client
        #msgQ.push([clientId,taskId,header.....])
        return 
    
    def send():
        while True:
            if clientID=-1:
                self.client.send()
            else:
                self.server.send()
            #get msg from returnMsgQ
            #if have clientId, return it


class Processor:
    msgQ=mp.queue
    taskQ=
    returnMsgQ=queue
    currentFunction=None
    functionList=[]
    def __init__(self) -> None:
        #init comfy
        mp.Process(self.msgHandling)
        pass

    def registerFunc(func):
        self.functionList.push(func)

    def msgHandling():
        while True:
            #make msg to task
            #push task to taskQ
            #start runing i2i or i2t
            result=functionList[idx]()#ai generating
            returnMsgQ.push(result)



#main: server msg loop, client msg loop, asycn send
#process: msgHandling

####################### package ==========================
#====================== example =========================
