from XComClient import ComClient


if __name__ == "__main__":
    comclient = ComClient()
    comclient.registerFunc("image2image")
    comclient.asServer("192.168.178.45", 8765)


