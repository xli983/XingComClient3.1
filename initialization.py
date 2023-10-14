import multiprocessing as mp

import asyncio
import json
import os
import main

def init():
    main.execute_prestartup_script()
    from comfy.cli_args import args
    if os.name == "nt":
        import logging
        logging.getLogger("xformers").addFilter(lambda record: 'A matching Triton is not available' not in record.getMessage())

    if __name__ == "__main__":
        if args.cuda_device is not None:
            os.environ['CUDA_VISIBLE_DEVICES'] = str(args.cuda_device)
            print("Set cuda device to:", args.cuda_device)

        import cuda_malloc
    from websockets.server import serve
    from task_processor import image_processor
    from main import cleanup_temp
    image = None