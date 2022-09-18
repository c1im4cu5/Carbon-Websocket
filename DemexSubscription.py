from DemexWebsocket import Demex_Websocket
import asyncio
import json
import os

class DemexConnect:
    def __init__(self):
        self.orders = []

    #On successful connection
    async def on_connect(self):
        return await demex.subscribe("Subscription", [f"orders:{'<SWTH ADDRESS>'}"])

    #Receiving feed from websocket
    async def on_receive(self, records: dict):

        #Check if "Channel" is in records (Initial response will be missing "Channel")
        if 'channel' in records:
            count = 0

            print("Channel: " + records['channel'])
            #Wallet Orders
            #Check if orders in record
            print("Verifying channel...")

            if 'orders:' in records['channel']:
                print("Order Channel Verified\nSearching order status...")
                #Load options.json file
                a = []
                el=[]
                with open("orders.json", "r") as read_file:
                    el = json.load(read_file)
                for d in records['result']:
                    #Increment count
                    count += 1
                    if d['status'] == 'open':
                        print("New Order. No Execution Required. Returning to monitor status...")
                    elif d['status'] == 'filled':
                        print("Filled Order\nGenerating new order")
                        if d['side'] == "sell":
                            if d['price'] == '9999900000.000000000000000000':
                                el.update(str(count): {"side": "buy", "qty": d['quantity'], "price": '0.97225'})
                            elif d['price'] == '9959900000.000000000000000000':
                                el.update(str(count): {"side": "buy", "qty": d['quantity'], "price": '0.96755'})
                            elif d['price'] == '9899900000.000000000000000000':
                                el.update(str(count): {"side": "buy", "qty": d['quantity'], "price": '0.96001'})
                            elif d['price'] == '9859900000.000000000000000000':
                                el.update(str(count): {"side": "buy", "qty": d['quantity'], "price": '0.95855'})
                            elif d['price'] == '9799900000.000000000000000000':
                                el.update(str(count): {"side": "buy", "qty": d['quantity'], "price": '0.94225'})
                        elif d['side']== "buy":
                            if d['price'] == '9722500000.000000000000000000':
                                el.update(str(count): {"side": "sell", "qty": d['quantity'], "price": '0.99999'})
                            elif d['price'] == '9675500000.000000000000000000':
                                el.update(str(count): {"side": "sell", "qty": d['quantity'], "price": '0.99599'})
                            elif d['price'] == '9600100000.000000000000000000':
                                el.update(str(count): {"side": "sell", "qty": d['quantity'], "price": '0.98999'})
                            elif d['price'] == '9585500000.000000000000000000':
                                el.update(str(count): {"side": "sell", "qty": d['quantity'], "price": '0.98599'})
                            elif d['price'] == '9422500000.000000000000000000':
                                el.update(str(count): {"side": "sell", "qty": d['quantity'], "price": '0.97999'})
                    elif d['status'] == 'closed':
                        print("Closed Order. No Execution Required. Returing to monitor status...")

                #Load options.json file
                #with open("orders.json", "w") as fout:
                    #json.dump(el, fout)



                print("Initiating Typescript Order File...")

                #Run ts-node file command line
                os.system("ts-node examples/create_orders.ts")


    async def main(self):
        #Gather tasks for running concurrently
        asyncio.gather(
                        asyncio.get_event_loop().run_until_complete(await demex.connect(self.on_receive, self.on_connect)),
                        )

if __name__ == "__main__":
    demex: Demex_Websocket = Demex_Websocket('wss://ws-api.carbon.network/ws')
    objName = DemexConnect()
    asyncio.run(objName.main())
