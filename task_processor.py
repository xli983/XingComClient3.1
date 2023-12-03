from init import *
from prompt_class import Prompt
import main
from main import cleanup_temp
from comfy.cli_args import args
from Interrupt import ProgressTracker
from reversePrompt.clip_interrogator import Config, Interrogator

class CrossProcess:
    interrupt=None

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



def i2i_processor(i2iQueue: mp.Queue, sendingMessage_queue: mp.Queue,state):
    i2i_init()
    e = execution.PromptExecutor()
    while True:
        if i2iQueue.empty():
            continue

        ProgressTracker.interrupter=state
        task_tuple = i2iQueue.get()
        image_data, config_data, client_id= task_tuple
        #sendingMessage_queue.put(("Start Processing your Image", client_id, "message"))

        try:
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
                sendingMessage_queue.put(("Canceled", client_id, "message"))
                continue

            #!!!!!!!!! for testing !!!!!!!!!
            image = image.resize(shape, Image.LANCZOS)
            #!!!!!!!!! for testing !!!!!!!!!
            
            image = image.convert('RGBA')
            result = image_to_png_bytestring(image.resize((shape[0], shape[1]), Image.LANCZOS))
            sendingMessage_queue.put((result,client_id,"image"))

        except Exception as e:
            print(f"Error: {e}")
            raise e
        
def i2t_processor(i2tQueue: mp.Queue, sendingMessage_queue: mp.Queue, state):
    ci = Interrogator(Config(clip_model_name="ViT-L-14/openai"))
    while True:
        if i2tQueue.empty():
            continue
        task_tuple = i2tQueue.get()
        image_data, client_id= task_tuple

        try:
            #image
            received = image_data
            image = decodePNG(received)
            prompt = ci.interrogate_fast(image)
            sendingMessage_queue.put((prompt,client_id,"prompt"))

        except Exception as e:
            print(f"Error: {e}")
            raise e
