import * as BIP39 from "bip39";
import { WSConnectorTypes } from "../lib";
import { CarbonSDK, WSConnector, WSChannel, WSResult} from "./_sdk";
import "./_setup";

(async () => {

  //Retrieve mnemonic from .env file
  const mnemonics = process.env.MNEMONICS ?? BIP39.generateMnemonic();

  //Print mnemonic to console
  console.log("mnemonics:", mnemonics);

  //Carbon SDK Instance
  const sdk = await CarbonSDK.instance({
    network: CarbonSDK.Network.MainNet,
  });

  //Connect SDK with Mnemonic
  const connectedSDK = await sdk.connectWithMnemonic(mnemonics);

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

    //Pull Object Data from result
    let res = result.data;

    //Print Data to console
    console.log("received orders", res);
  });

  // unsubscribe
  //await wsConnector.unsubscribe({ channel: WSChannel.orders });

  // clean up
  //await wsConnector.disconnect();
})();
