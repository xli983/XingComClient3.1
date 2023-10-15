from init import *
from prompt_class import Prompt

class CrossProcess:
    interrupt=None

def image_processor(task_queue: mp.Queue, sendingMessage_queue: mp.Queue,state):
    from nodes import init_custom_nodes
    init_custom_nodes()
    e = execution.PromptExecutor()
    from Interrupt import ProgressTracker
    ProgressTracker.interrupter=state
    while True:
        if task_queue.empty():
            continue

        task_tuple = task_queue.get()

        image_data, config_data, client_id= task_tuple
        sendingMessage_queue.put(("Start Processing your Image", client_id, "message"))

        try:
            ProgressTracker.interrupter.value=0
            #image
            received = image_data
            init_img: Image.Image
            init_img = decodePNG(received)
            shape = init_img.size
            image_handler.set_image_value(init_img)

            #mode
            prompt = Prompt(json_modes.test)
            execute_outputs = ['9']
            extra_data = json_modes.test_extra_data #maybe don't need
            prompt_id = '31de2ae1-c8c3-4dd0-85ff-d5fe017f9602' #change later

            #Lora
            LoraList = config_data.get('lora', None)
            if LoraList is not None and LoraList != []:
                prompt.add_lora(LoraList)
                prompt.link_lora(LoraList)
                

            #Configs - KSampler
            new_seed = random.randint(0, 2**32)
            prompt.update_attribute("KSampler", "seed", new_seed)
            prompt.update_attribute("KSampler", "cfg", float(config_data.get('cfg', '10')))
            prompt.update_attribute("KSampler", "denoise", float(config_data.get('intensity', '60')) * 0.01)

            #Configs - models
            if config_data.get('model', '') is None:
                prompt.update_attribute("CheckpointLoaderSimple", "ckpt_name", 'etherBluMix_etherBluMix5.safetensors')
            else:
                prompt.update_attribute("CheckpointLoaderSimple", "ckpt_name", config_data.get('model', 'etherBluMix_etherBluMix5.safetensors'))

            #Configs - prompt
            prompt.update_attribute("CLIPTextEncode", "text", "masterpiece, best quality," + config_data.get('prompt', ''))
            prompt.update_attribute("CLIPTextEncode_1", "text", "easynegative" + config_data.get('negPrompt', 'easynegative'))

            print(prompt.data)
            image = e.execute(prompt.data, prompt_id, extra_data, execute_outputs)
            if image == "Interrupted":
                sendingMessage_queue.put(("Canceled", client_id, "message"))
                continue
            
            image = image.convert('RGBA')
            result = image_to_png_bytestring(image.resize((shape[0], shape[1]), Image.LANCZOS))
            sendingMessage_queue.put((result,client_id,"image"))

        except Exception as e:
            print(f"Error: {e}")
            e = execution.PromptExecutor()
