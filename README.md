# Demex-Exchange-Websocket
Order Subscription Python Websocket for <https://app.dem.exchange> - IBC Enabled Blockchain App for 0xcarbon

Websocket is currently being designed to operate in conjunction with the Carbon SDK.

## Goal
Stable Pair Grid Bots (WBTC-BTCB, USDC-BUSD)

## Instructions for Order Generation
While the Python websocket can be easily run without the Carbon SDK, if you are looking to use the socket for order generation, the files will neeed to be uploaded to the Carbon SDK; which also means you will need to install it.

<https://github.com/Switcheo/carbon-js-sdk>

Remember to alter the .env.default file to the appropriate settings! When resaving it, save the file as ".env".

Furthermore, during the install process of the Carbon SDK, you may notice the install doesn't complete correctly. This is likely because you don't have the Cosmos SDK installed.

Filed labeled "create_orders.ts" should be uploaded to the examples file of the Carbon SDK. Files labeled orders.json, CarbonSubscription.py and CarbonWebsocket.py can be uploaded to the root directory of the SDK.

If you have troubles, please feel free to reach out to me via Telegram: <https://t.me/c1im4cu5>

## To-Do's
        - [x] Develop initial python socket
        - [x] Develop initial subscription
        - [x] Develop JSON structure for order generation
        - [x] Alter create_order.ts to pull data via JSON and generate order(s)
        - [ ] Further develop socket for more subscription options based on Carbon API
        - [ ] Build basic TS POST API to monitor for orders (Currently run haphazardly) and transition socket to http POST request for order generation

## Donations are Always Welcome
We appreciate the Carbon Community and are always thankful for any donations! Here is our "SWTH" Carbon Address: swth1dwdvy48exj22st0zvwk8s3k9tfnksrj9v7fhuu
