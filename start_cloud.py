from Xing_Comfy_processor import *

    
if __name__ == "__main__":
    comclient = ComClient()
    comclient.registerFunc(i2i)
    comclient.asClient()