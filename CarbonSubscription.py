from DemexWebsocket import Demex_Websocket
import asyncio
import requests
import json
import os

class DemexConnect:

    #On Object Initiation
    def __init__(self):

        #Define json headers for http orderbook request
        headers = {
            'accept': 'application/json',
        }

        #Get API request to Carbon Network for Orderbook snapshot
        response = requests.get('https://api.carbon.network/carbon/book/v1/books', headers=headers)

        #Respons to Json
        self.books = response.json()

        #Print Markets
        for i in self.books['books']:
            print(i['market'])

    #On successful connection
    async def on_connect(self):
        #Notes - On_Connect Subscription
        #User should remove the <SWTH ADDRESS> and input their own

        #Pools Subscription - Confirmed Working 5-10-22
        #return await demex.subscribe("Subscription", [f"pools"])

        #Subscribing to multiple channels (Orders and Books)
        #return await demex.subscribe("Subscription", [f"orders:{'<SWTH ADDRESS>'}", f"books:{'eth1_usdc1'}"])

        #Books subscription requires an initial request for a single orderbook; which has not yet been built
        #return await demex.subscribe("Subscription", [f"books:{'swth_usdc1'}"])

        #Books subscription - Multiple Markets
        #Built in preparation for orderbook monitoring
        #Notes - Orderbook Monitoring:
        #We retrieve the initial orderbook via http request on __init__ under self.books)
        return await demex.subscribe("Subscription", [
                                        f"books:{'swth_usdc1'}",
                                        f"books:{'swth_busd1'}",
                                        f"books:{'ETHUSDC_PERP'}",
                                        f"books:{'WBTCUSDC_PERP'}",
                                        f"books:{'eth1_usdc1'}",
                                        f"books:{'wbtc1_usdc1'}",
                                        f"books:{'eth1_wbtc1'}",
                                        f"books:{'wbtc1_btcb1'}",
                                        f"books:{'busd1_usdt1'}",
                                        f"books:{'AAVE_BUSD'}",
                                        f"books:{'APE_BUSD'}",
                                        f"books:{'ATOM_BUSD'}",
                                        f"books:{'ATOM_SWTH'}",
                                        f"books:{'EVMOS_BUSD'}",
                                        f"books:{'busd1_usdc1'}",
                                        f"books:{'bnb1_busd1'}",
                                        f"books:{'bnb1_eth1'}"
                                        ])

    #On successful connection
    async def on_error(self, err):
        #Unsubscribe on error
        print("Websocket Error...\n.............\n")
        print(err)
        print("Restarting Socket...\n")
        return await demex.unsubscribe("Subscription", [
                                        f"books:{'swth_usdc1'}",
                                        f"books:{'swth_busd1'}",
                                        f"books:{'ETHUSDC_PERP'}",
                                        f"books:{'WBTCUSDC_PERP'}",
                                        f"books:{'eth1_usdc1'}",
                                        f"books:{'wbtc1_usdc1'}",
                                        f"books:{'eth1_wbtc1'}",
                                        f"books:{'wbtc1_btcb1'}",
                                        f"books:{'busd1_usdt1'}",
                                        f"books:{'AAVE_BUSD'}",
                                        f"books:{'APE_BUSD'}",
                                        f"books:{'ATOM_BUSD'}",
                                        f"books:{'ATOM_SWTH'}",
                                        f"books:{'EVMOS_BUSD'}",
                                        f"books:{'busd1_usdc1'}",
                                        f"books:{'bnb1_busd1'}",
                                        f"books:{'bnb1_eth1'}"
                                        ])


    #Receiving feed from websocket
    async def on_receive(self, records: dict):

        #Check if "Channel" is in records (Initial response will be missing "Channel")
        if 'channel' in records:

            #Checking type of received message
            #Checking for orderbook message
            if 'books:' in records['channel']:
                print("Channel: Books\nUpdating Orderbook...")
                #Iterating over received dict
                for r in records['result']:
                    #Iterating over list value from key in dict
                    for m in self.books['books']:
                        #If message market = stored orderbook market
                        if  r['market'] == m['market']:
                            #If message side is buy
                            if r['side'] == 'buy':
                                print("BUY: ", r)
                                #Iterate over list of dicts (orderbook) - bids=buy
                                for i in m['bids']:
                                    #If message price equals bid dict price
                                    if r['price'] == i['price']:
                                        #If messae type is update
                                        if r['type'] == "update":
                                            #Update total_quantity of price by adding positive/negative
                                            i['total_quantity'] = str(float(i['total_quantity']) + float(r['quantity']))
                                        #If message type is new
                                        elif r['type'] == "new":
                                            #Append bids list with dict of newly added orderbook price and quantity
                                            #Notes:
                                            #Need to reorder sequence and/or insert into OrderedDict
                                            #Orders is left emptpy, but could be populated. Initial http response possesses order list with hashes as values
                                            m['bids'].append({"price" : r['price'], "total_quantity": r['quantity'], "orders": []})
                                        #If message type is delete
                                        elif r['type'] == "delete":
                                            #Delete dict from list in stored orderbook
                                            del i
                            #If message side is sell
                            if r['side'] == 'sell':
                                print("SELL: ", r)
                                #Iterate over list of dicts (orderbook) asks=sell
                                for i in m['asks']:
                                    #If message prices equals dict price
                                    if r['price'] == i['price']:
                                        #If message type is update
                                        if r['type'] == "update":
                                            #Update total_quantity of price by adding positive/negatives
                                            i['total_quantity'] = str(float(i['total_quantity']) + float(r['quantity']))
                                        #If message type is new
                                        elif r['type'] == "new":
                                            #Append asks list with dict of newly added orderbook price and quantity
                                            m['asks'].append({"price" : r['price'], "total_quantity": r['quantity'], "orders": []})
                                        #If message type is delete
                                        elif r['type'] == "delete":
                                            #Delete dict from list in orderbook
                                            del i


            if 'orders:' in records['channel']:
                print("Searching order status...")
                array : list = []
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
                                if d['price'] == "0.000000000001002500":
                                    array.append({"market": "busd1_usdc1", "side": "Buy", "qty": "95000000000000000000", "price": '0.000000000000996800'})
                                elif d['price'] == "0.000000000001000300":
                                    array.append({"market": "busd1_usdc1","side": "Buy", "qty": "20000000000000000000", "price":  "0.000000000000999000"})
                                elif d['price'] == "0.000000000001000600":
                                    array.append({"market": "busd1_usdc1","side": "Buy", "qty": "40000000000000000000", "price": "0.000000000000998600"})
                                elif d['price'] == "0.000000000001000900":
                                    array.append({"market": "busd1_usdc1","side": "Buy", "qty": "50000000000000000000", "price": "0.000000000000998200"})
                                elif d['price'] == "0.000000000001001300":
                                    array.append({"market": "busd1_usdc1","side": "Buy", "qty": "70000000000000000000", "price": "0.000000000000997800"})
                                elif d['price'] == "0.000000000001001900":
                                    array.append({"market": "busd1_usdc1","side": "Buy", "qty": "70000000000000000000", "price": "0.000000000000997400"})

                            elif d['side']== "buy":
                                if d['price'] == "0.000000000000996800":
                                    array.append({"market": "busd1_usdc1","side": "Sell", "qty": "95000000000000000000", "price": "0.000000000001002500"})
                                elif d['price'] == "0.000000000000999000":
                                    array.append({"market": "busd1_usdc1","side": "Sell", "qty": "20000000000000000000", "price": '0.000000000001000300'})
                                elif d['price'] == "0.000000000000998600":
                                    array.append({"market": "busd1_usdc1","side": "Sell", "qty": "40000000000000000000", "price": '0.000000000001000600'})
                                elif d['price'] == "0.000000000000998200":
                                    array.append({"market": "busd1_usdc1","side": "Sell", "qty": "50000000000000000000", "price": '0.000000000001000900'})
                                elif d['price'] == "0.000000000000997800":
                                    array.append({"market": "busd1_usdc1","side": "Sell", "qty": "70000000000000000000", "price": '0.000000000001001300'})
                                elif d['price'] == "0.000000000000997400":
                                    array.append({"market": "busd1_usdc1","side": "Sell", "qty": "70000000000000000000", "price": '0.000000000001001900'})

                            #Sending post request to ts server
                            print("Initiating Post Request to localhost:3000/trade")
                            requests.post(self.url, data=json.dumps(array), headers=headers)

                            #Notification of process end
                            print("Post request sent to server.")

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
