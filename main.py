import comfy.options
comfy.options.enable_args_parsing()

import os
import importlib.util
import folder_paths
import time
import time
import aioconsole

def execute_prestartup_script():
    def execute_script(script_path):
        module_name = os.path.splitext(script_path)[0]
        try:
            spec = importlib.util.spec_from_file_location(module_name, script_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return True
        except Exception as e:
            print(f"Failed to execute startup-script: {script_path} / {e}")
        return False

    node_paths = folder_paths.get_folder_paths("custom_nodes")
    for custom_node_path in node_paths:
        possible_modules = os.listdir(custom_node_path)
        node_prestartup_times = []

        for possible_module in possible_modules:
            module_path = os.path.join(custom_node_path, possible_module)
            if os.path.isfile(module_path) or module_path.endswith(".disabled") or module_path == "__pycache__":
                continue

            script_path = os.path.join(module_path, "prestartup_script.py")
            if os.path.exists(script_path):
                time_before = time.perf_counter()
                success = execute_script(script_path)
                node_prestartup_times.append((time.perf_counter() - time_before, module_path, success))
    if len(node_prestartup_times) > 0:
        print("\nPrestartup times for custom nodes:")
        for n in sorted(node_prestartup_times):
            if n[2]:
                import_message = ""
            else:
                import_message = " (PRESTARTUP FAILED)"
            print("{:6.1f} seconds{}:".format(n[0], import_message), n[1])
        print()

execute_prestartup_script()


# Main code
import asyncio
import itertools
import shutil
import threading
import gc

from comfy.cli_args import args

if os.name == "nt":
    import logging
    logging.getLogger("xformers").addFilter(lambda record: 'A matching Triton is not available' not in record.getMessage())

if __name__ == "__main__":
    if args.cuda_device is not None:
        os.environ['CUDA_VISIBLE_DEVICES'] = str(args.cuda_device)
        print("Set cuda device to:", args.cuda_device)

    if args.deterministic:
        if 'CUBLAS_WORKSPACE_CONFIG' not in os.environ:
            os.environ['CUBLAS_WORKSPACE_CONFIG'] = ":4096:8"

    import cuda_malloc

import comfy.utils
import yaml

import execution
import server
from server import BinaryEventTypes
from nodes import init_custom_nodes
import comfy.model_management

def cuda_malloc_warning():
    device = comfy.model_management.get_torch_device()
    device_name = comfy.model_management.get_torch_device_name(device)
    cuda_malloc_warning = False
    if "cudaMallocAsync" in device_name:
        for b in cuda_malloc.blacklist:
            if b in device_name:
                cuda_malloc_warning = True
        if cuda_malloc_warning:
            print("\nWARNING: this card most likely does not support cuda-malloc, if you get \"CUDA error\" please run ComfyUI with: --disable-cuda-malloc\n")


def prompt_worker(q, server):
    e = execution.PromptExecutor(server)
    last_gc_collect = 0
    need_gc = False
    gc_collect_interval = 10.0

    while True:
        timeout = 1000.0
        if need_gc:
            timeout = max(gc_collect_interval - (current_time - last_gc_collect), 0.0)

        queue_item = q.get(timeout=timeout)
        if queue_item is not None:
            print("queue item is not none")
            item, item_id = queue_item
            execution_start_time = time.perf_counter()
            prompt_id = item[1]
            server.last_prompt_id = prompt_id

            print(item[2])
            print(prompt_id)
            print(item[3])
            print(item[4])
            e.execute(item[2], prompt_id, item[3], item[4])
            print("e.execute commenced")
            need_gc = True
            q.task_done(item_id,
                        e.outputs_ui,
                        status=execution.PromptQueue.ExecutionStatus(
                            status_str='success' if e.success else 'error',
                            completed=e.success,
                            messages=e.status_messages))
            if server.client_id is not None:
                server.send_sync("executing", { "node": None, "prompt_id": prompt_id }, server.client_id)

            current_time = time.perf_counter()
            execution_time = current_time - execution_start_time
            print("Prompt executed in {:.2f} seconds".format(execution_time))

        flags = q.get_flags()
        free_memory = flags.get("free_memory", False)

        if flags.get("unload_models", free_memory):
            comfy.model_management.unload_all_models()
            need_gc = True
            last_gc_collect = 0

        if free_memory:
            e.reset()
            need_gc = True
            last_gc_collect = 0

        if need_gc:
            current_time = time.perf_counter()
            if (current_time - last_gc_collect) > gc_collect_interval:
                gc.collect()
                comfy.model_management.soft_empty_cache()
                last_gc_collect = current_time
                need_gc = False


async def input_loop():
    promptint = 100
    while True:
        user_input = await aioconsole.ainput("type something: ")  # Use aioconsole for async input
        if user_input == "0":  # Example command to stop the loop
            promptint += 1
            print("injecting queue")
            prompt_id = 'dfcd482a-4fe2-4643-8d0c-0b77f5edd' + str(promptint)
            print(prompt_id)
            outputs_to_execute = ['9']
            
            number = 1
            extra_data = {}
            server.prompt_queue.put((number, prompt_id, {'3': {'inputs': {'seed': promptint, 'steps': 20, 'cfg': 8.0, 'sampler_name': 'euler', 'scheduler': 'normal', 'denoise': 0.8200000000000001, 'model': ['4', 0], 'positive': ['6', 0], 'negative': ['7', 0], 'latent_image': ['5', 0]}, 'class_type': 'KSampler', '_meta': {'title': 'KSampler'}}, '4': {'inputs': {'ckpt_name': 'AnimeLineart_v10.ckpt'}, 'class_type': 'CheckpointLoaderSimple', '_meta': {'title': 'Load Checkpoint'}}, '5': {'inputs': {'width': 768, 'height': 768, 'batch_size': 1}, 'class_type': 'EmptyLatentImage', '_meta': {'title': 'Empty Latent Image'}}, '6': {'inputs': {'text': 'beautiful scenery nature glass bottle landscape, , purple galaxy bottle,', 'clip': ['4', 1]}, 'class_type': 'CLIPTextEncode', '_meta': {'title': 'CLIP Text Encode (Prompt)'}}, '7': {'inputs': {'text': 'text, watermark', 'clip': ['4', 1]}, 'class_type': 'CLIPTextEncode', '_meta': {'title': 'CLIP Text Encode (Prompt)'}}, '8': {'inputs': {'samples': ['3', 0], 'vae': ['4', 2]}, 'class_type': 'VAEDecode', '_meta': {'title': 'VAE Decode'}}, '9': {'inputs': {'filename_prefix': 'ComfyUI', 'images': ['8', 0]}, 'class_type': 'SaveImage', '_meta': {'title': 'Save Image'}}}, {'extra_pnginfo': {'workflow': {'last_node_id': 9, 'last_link_id': 12, 'nodes': [{'id': 8, 'type': 'VAEDecode', 'pos': [1209, 188], 'size': {'0': 210, '1': 46}, 'flags': {}, 'order': 5, 'mode': 0, 'inputs': [{'name': 'samples', 'type': 'LATENT', 'link': 7}, {'name': 'vae', 'type': 'VAE', 'link': 8}], 'outputs': [{'name': 'IMAGE', 'type': 'IMAGE', 'links': [9], 'slot_index': 0}], 'properties': {'Node name for S&R': 'VAEDecode'}}, {'id': 7, 'type': 'CLIPTextEncode', 'pos': [413, 389], 'size': {'0': 425.27801513671875, '1': 180.6060791015625}, 'flags': {}, 'order': 3, 'mode': 0, 'inputs': [{'name': 'clip', 'type': 'CLIP', 'link': 5}], 'outputs': [{'name': 'CONDITIONING', 'type': 'CONDITIONING', 'links': [6], 'slot_index': 0}], 'properties': {'Node name for S&R': 'CLIPTextEncode'}, 'widgets_values': ['text, watermark']}, {'id': 6, 'type': 'CLIPTextEncode', 'pos': [415, 186], 'size': {'0': 422.84503173828125, '1': 164.31304931640625}, 'flags': {}, 'order': 2, 'mode': 0, 'inputs': [{'name': 'clip', 'type': 'CLIP', 'link': 3}], 'outputs': [{'name': 'CONDITIONING', 'type': 'CONDITIONING', 'links': [4], 'slot_index': 0}], 'properties': {'Node name for S&R': 'CLIPTextEncode'}, 'widgets_values': ['beautiful scenery nature glass bottle landscape, , purple galaxy bottle,']}, {'id': 9, 'type': 'SaveImage', 'pos': [1509, 187], 'size': {'0': 210, '1': 270}, 'flags': {}, 'order': 6, 'mode': 0, 'inputs': [{'name': 'images', 'type': 'IMAGE', 'link': 9}], 'properties': {}, 'widgets_values': ['ComfyUI']}, {'id': 3, 'type': 'KSampler', 'pos': [863, 186], 'size': {'0': 315, '1': 262}, 'flags': {}, 'order': 4, 'mode': 0, 'inputs': [{'name': 'model', 'type': 'MODEL', 'link': 12}, {'name': 'positive', 'type': 'CONDITIONING', 'link': 4}, {'name': 'negative', 'type': 'CONDITIONING', 'link': 6}, {'name': 'latent_image', 'type': 'LATENT', 'link': 11}], 'outputs': [{'name': 'LATENT', 'type': 'LATENT', 'links': [7], 'slot_index': 0}], 'properties': {'Node name for S&R': 'KSampler'}, 'widgets_values': [357518788616362, 'randomize', 20, 8, 'euler', 'normal', 0.8200000000000001]}, {'id': 5, 'type': 'EmptyLatentImage', 'pos': [473, 609], 'size': {'0': 315, '1': 106}, 'flags': {}, 'order': 0, 'mode': 0, 'outputs': [{'name': 'LATENT', 'type': 'LATENT', 'links': [11], 'slot_index': 0}], 'properties': {'Node name for S&R': 'EmptyLatentImage'}, 'widgets_values': [768, 768, 1]}, {'id': 4, 'type': 'CheckpointLoaderSimple', 'pos': [26, 474], 'size': {'0': 315, '1': 98}, 'flags': {}, 'order': 1, 'mode': 0, 'outputs': [{'name': 'MODEL', 'type': 'MODEL', 'links': [12], 'slot_index': 0}, {'name': 'CLIP', 'type': 'CLIP', 'links': [3, 5], 'slot_index': 1}, {'name': 'VAE', 'type': 'VAE', 'links': [8], 'slot_index': 2}], 'properties': {'Node name for S&R': 'CheckpointLoaderSimple'}, 'widgets_values': ['AnimeLineart_v10.ckpt']}], 'links': [[3, 4, 1, 6, 0, 'CLIP'], [4, 6, 0, 3, 1, 'CONDITIONING'], [5, 4, 1, 7, 0, 'CLIP'], [6, 7, 0, 3, 2, 'CONDITIONING'], [7, 3, 0, 8, 0, 'LATENT'], [8, 4, 2, 8, 1, 'VAE'], [9, 8, 0, 9, 0, 'IMAGE'], [11, 5, 0, 3, 3, 'LATENT'], [12, 4, 0, 3, 0, 'MODEL']], 'groups': [], 'config': {}, 'extra': {}, 'version': 0.4}}, 'client_id': '7ba8772e213048d2a3a45949c30072eb'}, outputs_to_execute))
            # q.put((number, prompt_id, {'3': {'inputs': {'seed': 357518788616362, 'steps': 20, 'cfg': 8.0, 'sampler_name': 'euler', 'scheduler': 'normal', 'denoise': 0.8200000000000001, 'model': ['4', 0], 'positive': ['6', 0], 'negative': ['7', 0], 'latent_image': ['5', 0]}, 'class_type': 'KSampler', '_meta': {'title': 'KSampler'}}, '4': {'inputs': {'ckpt_name': 'AnimeLineart_v10.ckpt'}, 'class_type': 'CheckpointLoaderSimple', '_meta': {'title': 'Load Checkpoint'}}, '5': {'inputs': {'width': 768, 'height': 768, 'batch_size': 1}, 'class_type': 'EmptyLatentImage', '_meta': {'title': 'Empty Latent Image'}}, '6': {'inputs': {'text': 'beautiful scenery nature glass bottle landscape, , purple galaxy bottle,', 'clip': ['4', 1]}, 'class_type': 'CLIPTextEncode', '_meta': {'title': 'CLIP Text Encode (Prompt)'}}, '7': {'inputs': {'text': 'text, watermark', 'clip': ['4', 1]}, 'class_type': 'CLIPTextEncode', '_meta': {'title': 'CLIP Text Encode (Prompt)'}}, '8': {'inputs': {'samples': ['3', 0], 'vae': ['4', 2]}, 'class_type': 'VAEDecode', '_meta': {'title': 'VAE Decode'}}, '9': {'inputs': {'filename_prefix': 'ComfyUI', 'images': ['8', 0]}, 'class_type': 'SaveImage', '_meta': {'title': 'Save Image'}}}, {'extra_pnginfo': {'workflow': {'last_node_id': 9, 'last_link_id': 12, 'nodes': [{'id': 8, 'type': 'VAEDecode', 'pos': [1209, 188], 'size': {'0': 210, '1': 46}, 'flags': {}, 'order': 5, 'mode': 0, 'inputs': [{'name': 'samples', 'type': 'LATENT', 'link': 7}, {'name': 'vae', 'type': 'VAE', 'link': 8}], 'outputs': [{'name': 'IMAGE', 'type': 'IMAGE', 'links': [9], 'slot_index': 0}], 'properties': {'Node name for S&R': 'VAEDecode'}}, {'id': 7, 'type': 'CLIPTextEncode', 'pos': [413, 389], 'size': {'0': 425.27801513671875, '1': 180.6060791015625}, 'flags': {}, 'order': 3, 'mode': 0, 'inputs': [{'name': 'clip', 'type': 'CLIP', 'link': 5}], 'outputs': [{'name': 'CONDITIONING', 'type': 'CONDITIONING', 'links': [6], 'slot_index': 0}], 'properties': {'Node name for S&R': 'CLIPTextEncode'}, 'widgets_values': ['text, watermark']}, {'id': 6, 'type': 'CLIPTextEncode', 'pos': [415, 186], 'size': {'0': 422.84503173828125, '1': 164.31304931640625}, 'flags': {}, 'order': 2, 'mode': 0, 'inputs': [{'name': 'clip', 'type': 'CLIP', 'link': 3}], 'outputs': [{'name': 'CONDITIONING', 'type': 'CONDITIONING', 'links': [4], 'slot_index': 0}], 'properties': {'Node name for S&R': 'CLIPTextEncode'}, 'widgets_values': ['beautiful scenery nature glass bottle landscape, , purple galaxy bottle,']}, {'id': 9, 'type': 'SaveImage', 'pos': [1509, 187], 'size': {'0': 210, '1': 270}, 'flags': {}, 'order': 6, 'mode': 0, 'inputs': [{'name': 'images', 'type': 'IMAGE', 'link': 9}], 'properties': {}, 'widgets_values': ['ComfyUI']}, {'id': 3, 'type': 'KSampler', 'pos': [863, 186], 'size': {'0': 315, '1': 262}, 'flags': {}, 'order': 4, 'mode': 0, 'inputs': [{'name': 'model', 'type': 'MODEL', 'link': 12}, {'name': 'positive', 'type': 'CONDITIONING', 'link': 4}, {'name': 'negative', 'type': 'CONDITIONING', 'link': 6}, {'name': 'latent_image', 'type': 'LATENT', 'link': 11}], 'outputs': [{'name': 'LATENT', 'type': 'LATENT', 'links': [7], 'slot_index': 0}], 'properties': {'Node name for S&R': 'KSampler'}, 'widgets_values': [357518788616362, 'randomize', 20, 8, 'euler', 'normal', 0.8200000000000001]}, {'id': 5, 'type': 'EmptyLatentImage', 'pos': [473, 609], 'size': {'0': 315, '1': 106}, 'flags': {}, 'order': 0, 'mode': 0, 'outputs': [{'name': 'LATENT', 'type': 'LATENT', 'links': [11], 'slot_index': 0}], 'properties': {'Node name for S&R': 'EmptyLatentImage'}, 'widgets_values': [768, 768, 1]}, {'id': 4, 'type': 'CheckpointLoaderSimple', 'pos': [26, 474], 'size': {'0': 315, '1': 98}, 'flags': {}, 'order': 1, 'mode': 0, 'outputs': [{'name': 'MODEL', 'type': 'MODEL', 'links': [12], 'slot_index': 0}, {'name': 'CLIP', 'type': 'CLIP', 'links': [3, 5], 'slot_index': 1}, {'name': 'VAE', 'type': 'VAE', 'links': [8], 'slot_index': 2}], 'properties': {'Node name for S&R': 'CheckpointLoaderSimple'}, 'widgets_values': ['AnimeLineart_v10.ckpt']}], 'links': [[3, 4, 1, 6, 0, 'CLIP'], [4, 6, 0, 3, 1, 'CONDITIONING'], [5, 4, 1, 7, 0, 'CLIP'], [6, 7, 0, 3, 2, 'CONDITIONING'], [7, 3, 0, 8, 0, 'LATENT'], [8, 4, 2, 8, 1, 'VAE'], [9, 8, 0, 9, 0, 'IMAGE'], [11, 5, 0, 3, 3, 'LATENT'], [12, 4, 0, 3, 0, 'MODEL']], 'groups': [], 'config': {}, 'extra': {}, 'version': 0.4}}}, outputs_to_execute))
            



async def run(server, address='', port=8188, verbose=True, call_on_start=None):
    input_task = asyncio.create_task(input_loop())
    await asyncio.gather(server.start(address, port, verbose, call_on_start), server.publish_loop(), input_task)


def hijack_progress(server):
    def hook(value, total, preview_image):
        comfy.model_management.throw_exception_if_processing_interrupted()
        progress = {"value": value, "max": total, "prompt_id": server.last_prompt_id, "node": server.last_node_id}

        server.send_sync("progress", progress, server.client_id)
        if preview_image is not None:
            server.send_sync(BinaryEventTypes.UNENCODED_PREVIEW_IMAGE, preview_image, server.client_id)
    comfy.utils.set_progress_bar_global_hook(hook)


def cleanup_temp():
    temp_dir = folder_paths.get_temp_directory()
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir, ignore_errors=True)


def load_extra_path_config(yaml_path):
    with open(yaml_path, 'r') as stream:
        config = yaml.safe_load(stream)
    for c in config:
        conf = config[c]
        if conf is None:
            continue
        base_path = None
        if "base_path" in conf:
            base_path = conf.pop("base_path")
        for x in conf:
            for y in conf[x].split("\n"):
                if len(y) == 0:
                    continue
                full_path = y
                if base_path is not None:
                    full_path = os.path.join(base_path, full_path)
                print("Adding extra search path", x, full_path)
                folder_paths.add_model_folder_path(x, full_path)

#def setup_server_and_queue():
#loop = asyncio.new_event_loop()
#asyncio.set_event_loop(loop)

#penguinserver = server.PromptServer(loop)
#penguinq = execution.PromptQueue(penguinserver)

#penguinserver.prompt_queue = penguinq
#penguinserver.add_routes()  # Make sure this is a method call

#return penguinq, penguinserver




if __name__ == "__main__":
    if args.temp_directory:
        temp_dir = os.path.join(os.path.abspath(args.temp_directory), "temp")
        print(f"Setting temp directory to: {temp_dir}")
        folder_paths.set_temp_directory(temp_dir)
    cleanup_temp()

    # q, server = setup_server_and_queue()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    server = server.PromptServer(loop)
    q = execution.PromptQueue(server)

    extra_model_paths_config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "extra_model_paths.yaml")
    if os.path.isfile(extra_model_paths_config_path):
        load_extra_path_config(extra_model_paths_config_path)

    if args.extra_model_paths_config:
        for config_path in itertools.chain(*args.extra_model_paths_config):
            load_extra_path_config(config_path)

    init_custom_nodes()

    cuda_malloc_warning()

    server.add_routes()
    hijack_progress(server)


    # Adding the code to activate prompt_worker every now and then'


# Assuming necessary imports are already handled
# from your_script import PromptQueue, PromptServer
# import execution, comfy.model_management

    threading.Thread(target=prompt_worker, daemon=True, args=(q, server)).start()

    if args.output_directory:
        output_dir = os.path.abspath(args.output_directory)
        print(f"Setting output directory to: {output_dir}")
        folder_paths.set_output_directory(output_dir)

    #These are the default folders that checkpoints, clip and vae models will be saved to when using CheckpointSave, etc.. nodes
    folder_paths.add_model_folder_path("checkpoints", os.path.join(folder_paths.get_output_directory(), "checkpoints"))
    folder_paths.add_model_folder_path("clip", os.path.join(folder_paths.get_output_directory(), "clip"))
    folder_paths.add_model_folder_path("vae", os.path.join(folder_paths.get_output_directory(), "vae"))

    if args.input_directory:
        input_dir = os.path.abspath(args.input_directory)
        print(f"Setting input directory to: {input_dir}")
        folder_paths.set_input_directory(input_dir)

    if args.quick_test_for_ci:
        exit(0)

    call_on_start = None
    if args.auto_launch:
        def startup_server(address, port):
            import webbrowser
            if os.name == 'nt' and address == '0.0.0.0':
                address = '127.0.0.1'
            webbrowser.open(f"http://{address}:{port}")
        call_on_start = startup_server

    try:
        loop.run_until_complete(run(server, address=args.listen, port=args.port, verbose=not args.dont_print_server, call_on_start=call_on_start))
    except KeyboardInterrupt:
        print("\nStopped server")



cleanup_temp()
