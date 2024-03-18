import asyncio
import socket
from multiprocessing import Process, set_start_method
from Xing_Comfy_processor import *  # Assuming comfyui is a function to be run
from XComClient import ComClient
import main
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
    # Your async logic here, for example, starting the client
    await comclient.start()

def run_comclient(local_ip):
    print("\033[93m Local IP Address: " + local_ip + " \033[0m")
    comclient = ComClient([i2i], "server", local_ip, 8765)
    asyncio.run(async_run_comclient(comclient))

def run_comfyui():
    # Assuming comfyui is an asyncio-based UI, otherwise adjust accordingly
    # If comfyui is a synchronous function, it can be called directly without adjustments
    asyncio.run(main.comfyui())

if __name__ == "__main__":
    # Use "spawn" start method to avoid issues on Windows and to have a fresh Python interpreter for each process
    set_start_method("spawn")
    
    local_ip = get_local_ip()

    # Create processes for ComClient and comfyui
    comclient_process = Process(target=run_comclient, args=(local_ip,))
    comfyui_process = Process(target=run_comfyui)

    # Start the processes
    comclient_process.start()
    comfyui_process.start()

    # Wait for both processes to finish
    comfyui_process.join()
    comclient_process.join()
