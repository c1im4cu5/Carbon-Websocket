import os
from DemexWebsocket import Demex_Websocket
import asyncio

class DemexConnect:
    def __init__(self):
        pass

    #On successful connection
    async def on_connect(self):
        return await demex.subscribe("Subscription", [f"orders:{'<swth_address>'}"])

    #Receiving feed from websocket
    async def on_receive(self, records: dict):
        print(records)

    async def main(self):
        #Gather tasks for running concurrently
        asyncio.gather(
                        asyncio.get_event_loop().run_until_complete(await demex.connect(self.on_receive, self.on_connect)),
                        )

if __name__ == "__main__":
    demex: Demex_Websocket = Demex_Websocket('wss://ws-api.carbon.network/ws')
    objName = DemexConnect()
    asyncio.run(objName.main())
