from init import *
from nodes import init_custom_nodes
from prompt_class import Prompt

def image_processor(task_queue: mp.Queue, sendingMessage_queue: mp.Queue):
    init_custom_nodes()
    e = execution.PromptExecutor()
    while True:
        if task_queue.empty():
            continue

        task_tuple = task_queue.get()

        image_data, config_data, client_id= task_tuple
        sendingMessage_queue.put(("Start Processing your Image", client_id, "message"))

        try:
            #image
            received = image_data
            init_img: Image.Image
            init_img = decodePNG(received)
            shape = init_img.size
            image_handler.set_image_value(init_img)

            #mode
            prompt = Prompt(json_modes.test)
            execute_outputs = ['9']
            extra_data = json_modes.upscale_extra_data #maybe don't need
            prompt_id = '31de2ae1-c8c3-4dd0-85ff-d5fe017f9602' #change later

            #Lora
            # LoraList = config_data.get('lora', None)
            # if LoraList != None:
            #     prompt = add_Lora(prompt, LoraList)
            #     LoraNum = len(LoraList)
            #     prompt = json_modes.test
            #     prompt["6"]["inputs"]["clip"] = [str(22+LoraNum-1), 1]
            #     prompt["3"]["inputs"]["model"] = [str(22+LoraNum-1), 0]

            #Configs - KSampler
            new_seed = random.randint(0, 2**32)
            prompt.update_attribute("KSampler", "seed", new_seed)

            prompt.update_attribute("KSampler", "cfg", float(config_data.get('cfg', '10')))
            prompt.update_attribute("KSampler", "denoise", float(config_data.get('intensity', '60')) * 0.01)

            if config_data.get('model', '') is not None:
                prompt.update_attribute("CheckpointLoaderSimple", "ckpt_name", config_data.get('model', 'etherBluMix_etherBluMix5.safetensors'))

            prompt.update_attribute("CLIPTextEncode", "text", "masterpiece, best quality," + config_data.get('prompt', ''))
            prompt.update_attribute("CLIPTextEncode_1", "text", "easynegative" + config_data.get('negPrompt', 'easynegative'))

            print(prompt.data)
            image = e.execute(prompt.data, prompt_id, extra_data, execute_outputs)
            
            image = image.convert('RGBA')
            result = image_to_png_bytestring(image.resize((shape[0], shape[1]), Image.LANCZOS))
            sendingMessage_queue.put((result,client_id,"image"))

        except Exception as e:
            print(f"Error: {e}")
