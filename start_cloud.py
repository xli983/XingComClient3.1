from Xing_Comfy_processor import *
from XComClient import ComClient
    
if __name__ == "__main__":
    comclient = ComClient([i2i])
    comclient.asClient("wss://xing.art/com/")