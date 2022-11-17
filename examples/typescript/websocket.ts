import fetch from "node-fetch";
import * as BIP39 from "bip39";
import { WSConnectorTypes } from "./lib";
import { CarbonSDK, WSConnector, WSChannel, WSResult} from "./examples/_sdk";
import "./examples/_setup";

(async () => {

  //Pull Mnemonic from .env file and print to console
  const mnemonics = process.env.MNEMONICS ?? BIP39.generateMnemonic();
  console.log("Mnemonic: ", mnemonics);

  //Carbon.SDK connection instance
  const sdk = await CarbonSDK.instance({
    network: CarbonSDK.Network.MainNet,
    /*config: {
      tmRpcUrl: process.env.TRPC_ENDPOINT,
    },*/
  });

  //Connect SDK with mnemonic and print successful conn status
  const connectedSDK = await sdk.connectWithMnemonic(mnemonics);
  console.log("Carbon SDK Connected");

  //Print connected wallet to console
  console.log("Connected Wallet: ", connectedSDK.wallet.bech32Address);

  //Create Websocket Connector Instance
  const wsConnector = new WSConnector({
    endpoint: sdk.networkConfig.wsUrl,
    timeoutConnect: 5000,
    onStatusChange: (connected: boolean) => {
      console.log(`ws connection changed: ${connected ? 'connected' : 'disconnected'}`)
    },
  });

  //Run connect before executing any request/subscription
  //Connect Websocket
  await wsConnector.connect();

  //Subscribe to new channel - Orders (Which requires an address to monitor)
  await wsConnector.subscribe({ channel: WSChannel.orders, address: connectedSDK.wallet.bech32Address}, (result: WSResult<unknown>) => {

    //Console notification of order
    //console.log("Received Orders", result);

    //Pull Object Data from result
    const r = result.data;
    const s = JSON.stringify(r);
    const d = JSON.parse(s);

    const new_orders = []

    //Pull Result (list of orders)
    let orders = d.result;
    let order: keyof typeof orders;

    for (order in orders){
      if (orders[order]["status"] == "open"){
        console.log("Open Order Received. No action performed.");
      };
      if (orders[order]['status'] == "filled"){
        console.log("Filled Order\nPreparing New Order(s)");
        if (orders[order]['market'] == "busd1_usdc1"){
          if (orders[order]['side'] == "buy"){

          };
          if (orders[order]['side'] == "sell"){

          };
        };
        //new_orders.push({})
      };
      if (orders[order]['status'] == "closed"){
        console.log("Closed Order");
      };
      if (orders[order]['status'] == "cancelled"){
        console.log("Cancelled Order");
      };
    }

    /*fetch('http://localhost:8000/trade', {
      method: 'post',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(r)
    });*/
  });

  // unsubscribe
  //await wsConnector.unsubscribe({ channel: WSChannel.orders });

  // clean up
  //await wsConnector.disconnect();
})().catch(console.error);
