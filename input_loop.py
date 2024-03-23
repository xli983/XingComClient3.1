import main
import comfy.options
comfy.options.enable_args_parsing()

import os
import importlib.util
import folder_paths
import time
import time
import aioconsole
import shared
from multiprocessing import Process, set_start_method
import multiprocessing.shared_memory
import json
import struct
from multiprocessing import shared_memory
import asyncio
import itertools
import shutil
import threading
import gc
import time

from comfy.cli_args import args


def input_loop(server):
    promptint = 100
    while True:
        shared_memory = multiprocessing.shared_memory.SharedMemory(name="shared_memory_example")
        # Check the value of the shared memory
        value = bool(shared_memory.buf[0])
        time.sleep(1)
        if value:
            promptint += 1
            print("injecting queue")
            prompt_id = read_from_shared_memory("shared_memory_promptid")
            outputs_to_execute = read_from_shared_memory("shared_memory_promptoutput")   
            number = 1
            promptdata = read_from_shared_memory("shared_memory_prompt")
            extra_data = read_from_shared_memory("shared_memory_promptextradata")
            shared_memory.buf[0] = 0  # False
            print("printing input data")

            print(number, prompt_id, promptdata, outputs_to_execute)


            server.prompt_queue.put((number, prompt_id, promptdata, {'extra_pnginfo': {'workflow': extra_data}, 'client_id': '7ba8772e213048d2a3a45949c30072eb'}, outputs_to_execute))
            shared_memory.close()


def read_from_shared_memory(shm_name):
    # Attach to the existing shared memory
    shm = shared_memory.SharedMemory(name=shm_name)
    
    # Read content size and content
    content_size = struct.unpack('I', shm.buf[:4])[0]  # First 4 bytes for size
    serialized_data = shm.buf[4:4 + content_size].tobytes()  # Next bytes for content
    
    # Deserialize the JSON back into Python data
    data = json.loads(serialized_data.decode('utf-8'))
    
    # Cleanup and return data
    shm.close()
    return data
