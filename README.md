# Demex-Exchange-Websocket
Order Subscription Python Websocket for <https://app.dem.exchange> - IBC Enabled Blockchain App for 0xcarbon

Websocket is currently being designed to operate in conjunction with the Carbon SDK.

## Goal
Stable Pair Grid Bots (WBTC-BTCB, BUSD-USDC)

## Instructions for Order Generation
While the Python websocket can be easily run without the Carbon SDK, if you are looking to use the Websocket for order generation, the files will neeed to be uploaded to the Carbon SDK; which also means you will need to install it.

<https://github.com/Switcheo/carbon-js-sdk>

Remember to alter the .env.default file to the appropriate settings! When resaving it, save the file as ".env".

Furthermore, during the install process of the Carbon SDK, you may notice the install doesn't complete correctly. This is likely because you don't have the Cosmos SDK installed.

Files labeled CarbonSubscription.py and CarbonWebsocket.py should be placed together in the root directory.

File labeled create_orders.ts should be uploaded to the examples file of the Carbon SDK.

File labeled server.ts should be uploaded to the root directory of Carbon SDK.

Run TS Server in Terminal Window:
```
ts-node server.ts
```

Open new Terminal Window and Run CarbonSubscription.py
```
python app.py
```
If you have troubles, please feel free to reach out to me via Telegram: <https://t.me/c1im4cu5>

## Enhancements
        - [x] Develop initial python Websocket
        - [x] Develop initial subscription
        - [x] Develop JSON structure for order generation
        - [x] Alter create_order.ts to pull data via JSON and generate order(s)
        - [-] Further develop Websocket for more subscription options based on Carbon API
        - [x] Build basic TS POST API to monitor for orders (Currently run haphazardly) and transition Websocket to http POST request for order generation
        - [x] Subscription and maintaining complete 0xcarbon (Token: SWTH) orderbook
        - [-] Reformat price and quantity with base_precision and quote_precision - handlers.py
        - [ ] Requirements.txt for Python server
        - [ ] Transition Demex-Trading-Bot from c1im4cu5 (on-exchange arbitrage)

## Donations are Always Welcome
We appreciate the Carbon Community and are always thankful for any donations! Here is our "SWTH" Carbon Address: swth1dwdvy48exj22st0zvwk8s3k9tfnksrj9v7fhuu

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to added/altered.
