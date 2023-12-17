import multiprocessing as mp
import asyncio
import json
import os
import main
import websockets
from websockets.sync.client import connect
from websockets.server import serve
from main import cleanup_temp
from task_processor import i2i_processor, i2t_processor, CrossProcess

from init import *
from prompt_class import Prompt
import main
from main import cleanup_temp
from comfy.cli_args import args
from Interrupt import ProgressTracker
from reversePrompt.clip_interrogator import Config, Interrogator

class Task:
    def __init__(self, client_id, message):
        self.message = message
        self.client_id = client_id
        self.task_id =  message[10:20]
        self.byte_buffer = b""
        self.config_data = None
        self.header = message[:10].decode('utf-8').rstrip('\x00')
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
        #interrupt
        self.manager = mp.Manager()
        state=self.manager.Value("i",0)
        CrossProcess.interrupt=state
        state.value=0
        #functions
        self.functionList = []
        self.currentFunction=None

        self.MessageProcessor =mp.Process(target=self.task_processor, args=(self, self.taskQueue,state))
        pass

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
            
    async def asServer(self,ip, port):
        async with serve(self.handle_client, ip, port):
            await asyncio.Future() 

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
                taskObject = Task(client_id,message)
                func = self.functions.get(taskObject.header)
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
        print(f"Config Data: {task.config_data}")
    
    async def block(self,task):
        task.byteBuffer += task.message[20:]

    async def i2i(self,task):      
        task.byteBuffer += task.message[20:]
        task.taskQueue.put((task.byteBuffer, task.config_data, task.client_id, "image2image"))
        task.byteBuffer = b"" # clean buffer
    
    async def i2t(self,task):
        task.byteBuffer += task.message[20:]
        task.taskQueue.put((task.byteBuffer, task.config_data, task.client_id, "image2text"))
        task.byteBuffer = b"" # clean buffer

    async def cancel(self,task):
        CrossProcess.interrupt.value=1
        print(f"Client {self.websocket} requested an interrupt.")
    
    #--------------------------------------------------Com Functions end here ------------------------------------
    def task_processor(self, taskQueue: mp.Queue, returnMsgQ: mp.Queue,state):
        while True:
            if taskQueue.empty():
                continue
            task_tuple = taskQueue.get()
            image_data, config_data, client_id, task_type= task_tuple
            func = self.functionList.get(task_type)
            init = False
            if self.currentFunction is not task_type:
                self.currentFunction=task_type
                init = True
            if func:
                result=func(image_data, config_data, client_id, init,state)
            returnMsgQ.put(result,client_id,task_type)
    #------------------------------------------------Process Functions start here -----------------------------------
    def i2i_init():
        main.execute_prestartup_script()
        if os.name == "nt":
            import logging
            logging.getLogger("xformers").addFilter(lambda record: 'A matching Triton is not available' not in record.getMessage())

        if __name__ == "__main__":
            if args.cuda_device is not None:
                os.environ['CUDA_VISIBLE_DEVICES'] = str(args.cuda_device)
                print("Set cuda device to:", args.cuda_device)
        image = None
        cleanup_temp()
        from nodes import init_custom_nodes
        init_custom_nodes()

    def image2image(image_data, config_data, client_id, init,state):
        if init is False:
            i2i_init()
            e = execution.PromptExecutor()
        try:
            ProgressTracker.interrupter=state
            ProgressTracker.interrupter.value=0
            #image
            received = image_data
            init_img: Image.Image
            init_img = decodePNG(received)
            shape = init_img.size
            #!!!!!!!!!!FOR TESTING!!!!
            init_img = init_img.resize((int(shape[0] * 0.5), int(shape[1] * 0.5)), Image.LANCZOS)
            #!!!!!!!!!!FOR TESTING!!!!
            image_handler.set_image_value(init_img)

            #mode
            prompt = Prompt(json_modes.fast)
            execute_outputs = json_modes.fast_execute_outputs
            extra_data = json_modes.fast_extra_data
            prompt_id = '31de2ae1-c8c3-4dd0-85ff-d5fe017f9602' #change later

            #Lora
            LoraList = config_data.get('lora', None)

            if LoraList is not None and LoraList != []:
                prompt.add_lora(LoraList)
                prompt.link_lora(LoraList)
                

            #Configs - KSampler
            new_seed = random.randint(0, 2**32)
            # prompt.update_attribute("KSampler", "seed", new_seed)
            # prompt.update_attribute("KSampler", "cfg", float(config_data.get('cfg', '7')))
            # prompt.update_attribute("KSampler", "denoise", float(config_data.get('intensity', '60')) * 0.01)

            #Configs - models
            if config_data.get('model', '') is None:
                prompt.update_attribute("CheckpointLoaderSimple", "ckpt_name", 'etherBluMix_etherBluMix5.safetensors')
            else:
                prompt.update_attribute("CheckpointLoaderSimple", "ckpt_name", config_data.get('model', 'etherBluMix_etherBluMix5.safetensors'))

            #Configs - prompt
            prompt.append_attribute("CLIPTextEncode", "text", "masterpiece, best quality," + config_data.get('prompt', ''))
            prompt.append_attribute("CLIPTextEncode_1", "text", "easynegative" + config_data.get('negPrompt', 'easynegative'))

            print(prompt.data)
            image = e.execute(prompt.data, prompt_id, extra_data, execute_outputs)
            if image == "Interrupted":
                return("Canceled")

            #!!!!!!!!! for testing !!!!!!!!!
            image = image.resize(shape, Image.LANCZOS)
            #!!!!!!!!! for testing !!!!!!!!!
            
            image = image.convert('RGBA')
            result = image_to_png_bytestring(image.resize((shape[0], shape[1]), Image.LANCZOS))
            return(result)
        except Exception as e:
            print(f"Error: {e}")
            raise e
        
    def image2text(image_data, config_data, client_id, init,state):
        if init is False:
            ci = Interrogator(Config(clip_model_name="ViT-L-14/openai"))
        try:
            #image
            received = image_data
            image = decodePNG(received)
            prompt = ci.interrogate_fast(image)
            return(prompt)

        except Exception as e:
            print(f"Error: {e}")
            raise e

    #------------------------------------------------Process Functions end here -----------------------------------
    
    async def send(self):
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
        if task_type == "image2image":
            # first_client_id = self.positionInqueue.pop(0)
            # for i, client_id in enumerate(self.positionInqueue):
            #     otherWebsocket = self.clientIdList.get(client_id)
            #     if i != 0:
            #         await otherWebsocket.send(f"position: {i}")
            print(result)
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
        self.functionList.push(func)




