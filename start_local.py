from Xing_Comfy_processor import *

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        return f"Error occurred: {e}"
    
if __name__ == "__main__":
    local_ip = get_local_ip()
    print("\033[93m Local IP Address: "+local_ip+" \033[0m")
    comclient = ComClient()
    comclient.registerFunc(i2i)
    comclient.asServer(local_ip, 8765)