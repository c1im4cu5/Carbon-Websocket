# Demex-Exchange-Websocket
Order Subscription Python Websocket for <https://app.dem.exchange> - IBC Enabled Blockchain App for 0xcarbon

Websocket is currently being designed to operate in conjunction with the Carbon SDK.

## Goal
Stable Pair Grid Bots (WBTC-BTCB, USDC-BUSD)

## Instructions for Order Generation
While the Python websocket can be easily run without the Carbon SDK, if you are looking to use the socket for order generation, the files will neeed to be uploaded to the Carbon SDK; which also means you will need to install it.

<https://github.com/Switcheo/carbon-js-sdk>

Remember to alter the .env.default file to the appropriate settings! When resaving it, save the file as ".env". Furthermore, during the install process of the Carbon SDK, you may notice the install doesn't complete correctly. This is likely because you don't have the Cosmos SDK installed.

If you have troubles, please feel free to reach out to me via Telegram: <https://t.me/c1im4cu5>

## To-Do's
        - [x] Develop initial python socket
        - [x] Develop initial subscription
        - [x] Develop JSON structure for order generation
        - [ ] Alter create_order.ts to pull data via JSON and generate order(s)
        - [ ] Further develop socket for more subscription options based on Carbon API


File is set to monitor the "orders" of the user's wallet address in preparation for a simple grid bot.

## Donations are Always Welcome
We appreciate the Carbon Community and are always thankful for any donations! Here is our "SWTH" Carbon Address: swth1dwdvy48exj22st0zvwk8s3k9tfnksrj9v7fhuu
