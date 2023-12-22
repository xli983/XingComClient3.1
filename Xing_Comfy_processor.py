
from XComClient import ComClient
import socket
from init import *
if mp.current_process().name == "taskProcessor":
    import traceback
    import execution
    import image_handler
    from prompt_class import Prompt
    import main
    from main import cleanup_temp
    from comfy.cli_args import args
    from Interrupt import ProgressTracker
    from reversePrompt.clip_interrogator import Config, Interrogator


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

def i2i(client_data, message):
    global comfyInited
    global executor
    global current_model
    ProgressTracker.interrupter=False
    if not comfyInited:
        comfy_init()
        executor = execution.PromptExecutor()
        comfyInited = True
        
    # ProgressTracker.interrupter=state
    # ProgressTracker.interrupter.value=0
    #image
    try:
        config=client_data["config"]
        init_img: Image.Image
        init_img = decodePNG(message)
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
        LoraList = config["lora"]

        if LoraList is not None and LoraList != []:
            prompt.add_lora(LoraList)
            prompt.link_lora(LoraList)
            

        #Configs - KSampler
        new_seed = random.randint(0, 2**32)
        # prompt.update_attribute("KSampler", "seed", new_seed)
        # prompt.update_attribute("KSampler", "cfg", float(config_data.get('cfg', '7')))
        # prompt.update_attribute("KSampler", "denoise", float(config_data.get('intensity', '60')) * 0.01)

        #Configs - models
        model = config['model']
        if model == None or model == "":
            model = "etherBluMix_etherBluMix5.safetensors"
        if current_model != model:
            current_model = model
            prompt.update_attribute("CheckpointLoaderSimple", "ckpt_name", model)

        #Configs - prompt
        pos_prompt = config['prompt']
        neg_prompt = config["negPrompt"]
        prompt.append_attribute("CLIPTextEncode", "text", "masterpiece, best quality," + pos_prompt)
        prompt.append_attribute("CLIPTextEncode_1", "text", "easynegative" + neg_prompt)

        print(prompt.data)
        image = executor.execute(prompt.data, prompt_id, extra_data, execute_outputs)
        if image == "Interrupted":
            return("Canceled")

        #!!!!!!!!! for testing !!!!!!!!!
        image = image.resize(shape, Image.LANCZOS)
        #!!!!!!!!! for testing !!!!!!!!!
        
        image = image.convert('RGBA')
        result = image_to_png_bytestring(image.resize((shape[0], shape[1]), Image.LANCZOS))
        return(result)
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
    



