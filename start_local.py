from XComClient import ComClient
import socket

def get_local_ip():
    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # No need to connect to a specific server
        # Using Google's public DNS server address and an arbitrary port number
        s.connect(("8.8.8.8", 80))
        # Get the IP address of the socket's local endpoint
        ip = s.getsockname()[0]
        # Close the socket
        s.close()
        return ip
    
    except Exception as e:
        return f"Error occurred: {e}"


if __name__ == "__main__":
    local_ip = get_local_ip()
    print(f"Local IP Address: {local_ip}")
    comclient = ComClient()
    comclient.registerFunc("image2image")
    comclient.asServer(local_ip, 8765)


