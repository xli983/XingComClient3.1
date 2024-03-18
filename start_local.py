import threading
import asyncio
from Xing_Comfy_processor import *
from XComClient import ComClient
import socket
from main import *

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        return f"Error occurred: {e}"

def run_comclient(local_ip):
    print("\033[93m Local IP Address: " + local_ip + " \033[0m")

    # Create and set a new event loop in the thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    comclient = ComClient([i2i], "server", local_ip, 8765)

def run_comfyui():
    comfyui()

if __name__ == "__main__":
    local_ip = get_local_ip()

    # Create threads for ComClient and comfyui
    comclient_thread = threading.Thread(target=run_comclient, args=(local_ip,))
    comfyui_thread = threading.Thread(target=run_comfyui)

    # Start the threads
    comclient_thread.start()
    comfyui_thread.start()
    
    # Wait for both threads to finish
    comfyui_thread.join()
    comclient_thread.join()
