from init import *
from AlphaProcessor import preprocess_image, postprocess_image
import PIL
from XingQueue import *
import shared
import time
import multiprocessing.shared_memory
from multiprocessing import Manager, shared_memory
import start_local
import json
import struct


if mp.current_process().name == "taskProcessor":
    import traceback
    import execution
    import image_handler
    from prompt_class import Prompt
    import main
    from main import cleanup_temp
    from comfy.cli_args import args
    from Interrupt import ProgressTracker
    # from reversePrompt.clip_interrogator import Config, Interrogator


def comfy_init():
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

comfyInited = False
executor = None
current_model = None
current_lora = None




def i2i(client_data, message):
    global comfyInited
    global executor
    global current_model
    ProgressTracker.interrupter=False
        
    # ProgressTracker.interrupter=state
    # ProgressTracker.interrupter.value=0
    #image

    try:
        config=client_data["config"]
        init_img: Image.Image
        init_img = decodePNG(message)
        init_img = init_img.convert("RGBA")

        # init_img = preprocess_image(init_img)
        
        shape = init_img.size
        init_img = init_img.resize((int(shape[0] * 1), int(shape[1] * 1)), Image.LANCZOS)

        init_img.save("input/preprocesstest.png")
        image_handler.set_image_value(init_img)

        #mode
        prompt = Prompt(json_modes.SDXL)
        execute_outputs = json_modes.SDXL_outputs
        extra_data = json_modes.SDXL_data
        prompt_id = '31de2ae1-c8c3-4dd0-85ff-d5fe017f9602' #change later

        #Lora
        LoraList = config["lora"]

        if LoraList is not None and LoraList != [] and LoraList != current_lora:
            prompt.add_lora(LoraList)
            prompt.link_lora(LoraList)

        current_lora = LoraList
            


        #Configs - KSampler
        new_seed = random.randint(0, 2**32)
        prompt.update_attribute("KSampler", "seed", new_seed)
        prompt.update_attribute("KSampler", "cfg", float(config['cfg']))
       # prompt.update_attribute("KSampler", "denoise",  float(config['intensity']) * 0.01)

        #Configs - models
        # model = config['model']
        # if model == None or model == "":
        #     model = "SDXLAnimeBulldozer_v10.safetensors"
        # if current_model != model:
        #     current_model = model
        #     prompt.update_attribute("CheckpointLoaderSimple", "ckpt_name", model)

        #Configs - prompt
        pos_prompt = config['prompt']
        print("positive prompt test")
        print("positive prompt is" + pos_prompt)
        neg_prompt = config["negPrompt"]
        pos_position = prompt.get_prompt_position('positive')
        neg_position = prompt.get_prompt_position('negative')
        print(pos_position)
        prompt.update_prompt(pos_position, "masterpiece, best quality," + pos_prompt)
        prompt.update_prompt(neg_position, "easynegative" + neg_prompt)


    
        shared.prompt = prompt.data, {'extra_pnginfo': {'workflow': extra_data}, 'client_id': '7ba8772e213048d2a3a45949c30072eb'}
        shared.prompt_id = prompt_id
        shared.outputs_to_execute = execute_outputs


        write_to_shared_memory("shared_memory_prompt", prompt.data)
        write_to_shared_memory("shared_memory_promptid", prompt_id)
        write_to_shared_memory("shared_memory_promptoutput", execute_outputs)
        write_to_shared_memory("shared_memory_promptextradata", extra_data)

        shared_memory = multiprocessing.shared_memory.SharedMemory(name="shared_memory_example")
        shared_memory.buf[0] = 1  # True
        shared_memory.close()


        while True:
            shared_memoryoutput = multiprocessing.shared_memory.SharedMemory(name="output_here")
            # Check the value of the shared memory
            value = bool(shared_memoryoutput.buf[0])
            if value:
                shared_memoryoutput.buf[0] = 0  # False
                image = Image.open("output/XingOutput.png")

                image = image.resize(shape, Image.LANCZOS)

                # image = postprocess_image(image)
                image = image.convert("RGBA")

                result = image_to_png_bytestring(image.resize((shape[0], shape[1]), Image.LANCZOS))

                return result
            else:
                time.sleep(0.5)

        
        return None

    except Exception as e:
        print(traceback.format_exc())
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
    


def write_to_shared_memory(shm_name, data):
    # Serialize data to JSON and encode it to bytes
    serialized_data = json.dumps(data).encode('utf-8')
    content_size = len(serialized_data)
    
    # Ensure the serialized data will fit in our 1MB shared memory segment
    assert content_size <= (1024 * 1024 - 4), "Serialized data exceeds 1MB limit"
    
    # Create or get a reference to the shared memory
    try:
        # Try to attach to an existing shared memory segment
        shm = shared_memory.SharedMemory(name=shm_name)
    except FileNotFoundError:
        # If the shared memory does not exist, create it
        shm = shared_memory.SharedMemory(name=shm_name, create=True, size=1024 * 1024)
    
    
    # Write the content size and content to the shared memory
    shm.buf[:4] = struct.pack('I', content_size)  # Content size as unsigned int
    shm.buf[4:4 + content_size] = serialized_data  # Serialized content
    
    # Cleanup: only do shm.close() here; shm.unlink() should be done when you're sure it's no longer needed
    shm.close()
    



