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
        time.sleep(2)
        print(value)
        if value:
            promptint += 1
            print("injecting queue")
            prompt_id = shared.prompt_id
            outputs_to_execute = ['9']      
            number = 1
            promptdata = shared.prompt
            extra_data = {}
            shared_memory.buf[0] = 0  # False
            print("printing input data")
            print(number, prompt_id, promptdata, outputs_to_execute)
            server.prompt_queue.put((number, prompt_id, promptdata, outputs_to_execute))
            shared_memory.close()
