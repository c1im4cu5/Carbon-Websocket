# Websocket Examples with API Post Request
I've built different language websocket channel subscriptions. The Carbon SDK is written in TS/JS. There are no other languages for which it has been translated. This section will cover order subscription examples for Python and TS. Please remember the files are meant to be used in conjunction with the Carbon SDK. Please follow the link and install it prior to beginning any of the listed processes. You will need to upload all documents to the directory upon successful installation.

<https://github.com/Switcheo/carbon-js-sdk>

### Notes to Carbon SDK Installation
Carbon SDK is not an easy install. If you encounter any troubles, it is likely because the Cosmos SDK is not installed. Since the 0xcarbon blockchain is an offshoot of the Cosmos blockchain, the Cosmos SDK is a required install prior to successful installation of the Carbon SDK.

Once you've managed to install the SDK, you will need to alter the .env.default file to the appropriate parameters. After alteration, please resave the file as ".env"

## API Folder
Whether using Python example or typescript example files, two terminal windows must currently be run to avoid second level async issues involved with order generation. I'm in the process of finding resolution to this issue. In the meantime, a typescript api server is run in a separate terminal window for localhost:3000

The API folder holds the files necessary to run the order generation server.

- create_orders.ts file should be uploaded to ./examples/ of the Carbon SDK
- server.ts file should be uploaded to the root director of the SDK

Navigate to the root directory of the Carbon SDK:
```
ts-node server.ts
```

## Option 1: Python Websocket Subscription with Typescript API
All files for the python websocket can be uploaded to the root directory of the Carbon SDK. In order to retrieve a connection to your Carbon Address (swth*), please review the on_connect function inside CarbonSubscription.py; which will assist you in applying the correct channel subscriptions.

```
python CarbonSubscription.py
```

### Enhancements to Python
        - [x] Develop initial python Websocket
        - [x] Develop initial subscription
        - [x] Develop JSON structure for order generation
        - [x] Further develop Websocket for more subscription options based on Carbon API
        - [x] Subscription and maintaining complete 0xcarbon (Token: SWTH) orderbook
        - [-] Reformat price and quantity with base_precision and quote_precision - handlers.py
        - [ ] Requirements.txt for Python server
        - [ ] Transition Demex-Trading-Bot from c1im4cu5 (on-exchange arbitrage)


## Option 2: Typescript Websocket Subscription with Typescript API
The single file, websocket.ts, can be uploaded to the root directory of the Carbon SDK. It is currently incomplete. See Enhancements section.

```
ts-node server.ts
```

### Enhancements to Typescript
        - [x] Develop channel subscription based on TS
        - [-] Develop JSON structure for order generation
        - [ ] Subscription and maintaining complete 0xcarbon (Token: SWTH) orderbook
        - [ ] Reformat price and quantity with base_precision and quote_precision - handlers.py

## Donations are Always Welcome
We appreciate the Carbon Community and are always thankful for any donations! Here is our "SWTH" Carbon Address: swth1dwdvy48exj22st0zvwk8s3k9tfnksrj9v7fhuu

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to added/altered.
