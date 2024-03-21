import asyncio
import socket
from multiprocessing import Process, set_start_method
import multiprocessing.shared_memory
from Xing_Comfy_processor import *  # Assuming comfyui is a function to be run
from XComClient import ComClient
import main
import threading
import input_loop
from input_loop import input_loop
# Assuming i2i and other necessary imports are correctly set in XComClient and Xing_Comfy_processor

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        return f"Error occurred: {e}"

async def async_run_comclient(comclient):
    await comclient.start()

def run_comclient(local_ip):
    print("\033[93m Local IP Address: " + local_ip + " \033[0m")
    comclient = ComClient([i2i], "server", local_ip, 8765)
    asyncio.run(async_run_comclient(comclient))

def run_comfyui_in_thread(q, server, loopr):
    def thread_target():
        asyncio.set_event_loop(asyncio.new_event_loop())  # New event loop for this thread
        main.comfyui(q, server, loop)
    
    thread = threading.Thread(target=thread_target)
    thread.start()
    return thread

def run_inputloop_in_thread(server):
    def thread_target():
        asyncio.set_event_loop(asyncio.new_event_loop())  # New event loop for this thread
        input_loop(server)  # Adjust as needed for your implementation
    
    thread = threading.Thread(target=thread_target)
    thread.start()
    return thread


if __name__ == "__main__":
    q, server, loop = main.setup_server_and_queue()

    shared_memory = multiprocessing.shared_memory.SharedMemory(create=True, size=1, name="shared_memory_example")
    shared_memory.buf[0] = 0  # False

    shared_memory_prompt = multiprocessing.shared_memory.SharedMemory(create=True, size=1024 * 1024, name="shared_memory_prompt")
    # shared_memory_prompt.buf[0] = 0  # False

    shared_memory_promptid = multiprocessing.shared_memory.SharedMemory(create=True, size=1024 * 1024, name="shared_memory_promptid")
    # shared_memory_prompt.buf[0] = 0  # False

    shared_memory_promptoutput = multiprocessing.shared_memory.SharedMemory(create=True, size=1024 * 1024, name="shared_memory_promptoutput")
    # shared_memory_prompt.buf[0] = 0  # False

    shared_memory_promptextradata = multiprocessing.shared_memory.SharedMemory(create=True, size=1024 * 1024, name="shared_memory_promptextradata")
    # shared_memory_prompt.buf[0] = 0  # False

    
    local_ip = get_local_ip()

    comclient_process = Process(target=run_comclient, args=(local_ip,))
    comfyui_thread = run_comfyui_in_thread(q, server, loop)
    inputloop_thread = run_inputloop_in_thread(server)


    comclient_process.start()

    comclient_process.join()
