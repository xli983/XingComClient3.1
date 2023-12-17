from XComClient import ComClient
import asyncio

if __name__ == "__main__":
    comclient = ComClient()
    asyncio.run(comclient.asServer("192.168.178.45", 8765))

