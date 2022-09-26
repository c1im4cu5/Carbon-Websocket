from DemexWebsocket import Demex_Websocket
from collections import OrderedDict
import asyncio
import requests
import json
import os

class DemexConnect:
    def __init__(self):
        headers = {
            'accept': 'application/json',
        }
        response = requests.get('https://api.carbon.network/carbon/book/v1/books', headers=headers)
        self.books = response.json()
        print(self.books)

        for i in self.books['books']:
            print(i['market'])

    #On successful connection
    async def on_connect(self):
        #User should remove the <SWTH ADDRESS> and input their own
        #Multiple examples of different subscriptions
        return await demex.subscribe("Subscription", [f"orders:{'swth1dwdvy48exj22st0zvwk8s3k9tfnksrj9v7fhuu'}", f"books:{'eth1_usdc1'}"])
        #return await demex.subscribe("Subscription", [f"market_stats:{'swth_usdc1'}"])
        #return await demex.subscribe("Subscription", [f"balances:{'swth1dwdvy48exj22st0zvwk8s3k9tfnksrj9v7fhuu'}"])

        #Books subscription requires an initial request; which has not yet been built
        #return await demex.subscribe("Subscription", [f"books:{'swth_usdc1'}"])

    #On successful connection
    async def on_error(self, err):
        #Unsubscribe on error
        print("Websocket Error...\n.............\n")
        print(err)
        print("Restarting Socket...\n")
        demex: Demex_Websocket = Demex_Websocket('wss://ws-api.carbon.network/ws')
        objName = DemexConnect()
        asyncio.run(objName.main())


    #Receiving feed from websocket
    async def on_receive(self, records: dict):

        print(records)

        #Check if "Channel" is in records (Initial response will be missing "Channel")
        if 'channel' in records:
            count = 0

            print("Channel: " + records['channel'])
            #Wallet Orders
            #Check if orders in record
            print("Verifying channel...")

            if 'books:' in records['channel']:

                print("Channel: Books\nUpdating Orderbook...")
                """for r in records['result']:
                    for d in self.books:
                        #bid = Buy
                        #ask = sell
                        if  r['market'] == d['market']:
                            if r['side'] == 'buy':
                                for i in d['bids']:"""




            if 'orders:' in records['channel']:
                print("Channel: Order\nSearching order status...")
                #Load options.json file
                el= OrderedDict()
                with open("orders.json", "r") as read_file:
                    array = json.load(read_file, object_pairs_hook=OrderedDict)
                for d in records['result']:

                    if d['status'] == 'open':
                        print("New Order. No Execution Required. Returning to monitor status...")
                    elif d['status'] == 'filled':
                        #Increment count
                        count += 1

                        print("Filled Order\nGenerating new order")

                        #Search if orders are wbtc_btcb
                        if d['market'] == "wbtc1_btcb1":

                            #Search if orders are buy vs sell
                            if d['side'] == "sell":
                                if d['price'] == '9999900000.000000000000000000':
                                    array.append({"market": "wbtc_btcb1", "side": "Buy", "qty": d['quantity'], "price": '0.97225'})
                                elif d['price'] == '9959900000.000000000000000000':
                                    array.append({"market": "wbtc_btcb1","side": "Buy", "qty": d['quantity'], "price": '0.96755'})
                                elif d['price'] == '9899900000.000000000000000000':
                                    array.append({"market": "wbtc_btcb1","side": "Buy", "qty": d['quantity'], "price": '0.96001'})
                                elif d['price'] == '9859900000.000000000000000000':
                                    array.append({"market": "wbtc_btcb1","side": "Buy", "qty": d['quantity'], "price": '0.95855'})
                                elif d['price'] == '9799900000.000000000000000000':
                                    array.append({"market": "wbtc_btcb1","side": "Buy", "qty": d['quantity'], "price": '0.94225'})
                            elif d['side']== "buy":
                                if d['price'] == '9722500000.000000000000000000':
                                    array.append({"market": "wbtc_btcb1","side": "Sell", "qty": d['quantity'], "price": '0.99999'})
                                elif d['price'] == '9675500000.000000000000000000':
                                    array.append({"market": "wbtc_btcb1","side": "Sell", "qty": d['quantity'], "price": '0.99599'})
                                elif d['price'] == '9600100000.000000000000000000':
                                    array.append({"market": "wbtc_btcb1","side": "Sell", "qty": d['quantity'], "price": '0.98999'})
                                elif d['price'] == '9585500000.000000000000000000':
                                    array.append({"market": "wbtc_btcb1","side": "Sell", "qty": d['quantity'], "price": '0.98599'})
                                elif d['price'] == '9422500000.000000000000000000':
                                    array.append({"market": "wbtc_btcb1","side": "Sell", "qty": d['quantity'], "price": '0.97999'})

                        #Search if orders are busd_usdc
                        elif d['market'] == "busd1_usdc1":

                            #Search if orders are buy vs sell:
                            if d['side'] == "sell":
                                # price =0.995 = "0.000000000000995000"
                                # qty = $1.00 USDC = "1000000000000000000"
                                if d['price'] == "0.000000000001001500":
                                    array.append({"market": "busd1_usdc1", "side": "Buy", "qty": "95000000000000000000", "price": '0.000000000000996800'})
                                elif d['price'] == "0.000000000000999900":
                                    array.append({"market": "busd1_usdc1","side": "Buy", "qty": "20000000000000000000", "price":  "0.000000000000999000"})
                                elif d['price'] == "0.000000000001000200":
                                    array.append({"market": "busd1_usdc1","side": "Buy", "qty": "40000000000000000000", "price": "0.000000000000998600"})
                                elif d['price'] == "0.000000000001000500":
                                    array.append({"market": "busd1_usdc1","side": "Buy", "qty": "50000000000000000000", "price": "0.000000000000998200"})
                                elif d['price'] == "0.000000000001000800":
                                    array.append({"market": "busd1_usdc1","side": "Buy", "qty": "70000000000000000000", "price": "0.000000000000997800"})
                                elif d['price'] == "0.000000000001001100":
                                    array.append({"market": "busd1_usdc1","side": "Buy", "qty": "70000000000000000000", "price": "0.000000000000997400"})

                            elif d['side']== "buy":
                                if d['price'] == "0.000000000000996800":
                                    array.append({"market": "busd1_usdc1","side": "Sell", "qty": "95000000000000000000", "price": "0.000000000001001500"})
                                elif d['price'] == "0.000000000000999000":
                                    array.append({"market": "busd1_usdc1","side": "Sell", "qty": "20000000000000000000", "price": '0.000000000000999900'})
                                elif d['price'] == "0.000000000000998600":
                                    array.append({"market": "busd1_usdc1","side": "Sell", "qty": "40000000000000000000", "price": '0.000000000001000200'})
                                elif d['price'] == "0.000000000000998200":
                                    array.append({"market": "busd1_usdc1","side": "Sell", "qty": "50000000000000000000", "price": '0.000000000001000500'})
                                elif d['price'] == "0.000000000000997800":
                                    array.append({"market": "busd1_usdc1","side": "Sell", "qty": "70000000000000000000", "price": '0.000000000001000800'})
                                elif d['price'] == "0.000000000000997400":
                                    array.append({"market": "busd1_usdc1","side": "Sell", "qty": "70000000000000000000", "price": '0.000000000001001100'})

                            #Load options.json file
                            with open("orders.json", "w") as fout:
                                json.dump(array, fout)

                            print("Initiating Typescript Order File...")

                            #Run ts-node file command line
                            os.system("ts-node examples/create_orders.ts")

                    elif d['status'] == 'closed':
                        print("Closed Order. No Execution Required. Returing to monitor status...")

    async def main(self):
        #Gather tasks for running concurrently
        asyncio.gather(
                        asyncio.get_event_loop().run_until_complete(await demex.connect(self.on_receive, self.on_connect, self.on_error)),
                        )

if __name__ == "__main__":
    demex: Demex_Websocket = Demex_Websocket('wss://ws-api.carbon.network/ws')
    objName = DemexConnect()
    asyncio.run(objName.main())
