import { BigNumber } from "bignumber.js";
import * as BIP39 from "bip39";
import { OrderModule } from "../lib";
import { MsgCreateOrder } from "../lib/codec/order/tx";
import { CarbonTx } from "../lib/util";
import { CarbonSDK } from "./_sdk";
import "./_setup";
import { ServerResponse, IncomingMessage } from "http";


const performTrades = (req: IncomingMessage, res: ServerResponse) => {
  // Read the data from the request
  let data = "";

  req.on("data", (chunk) => {
    //Parserequest data into string
    data += chunk.toString();
  });

  // When the request is done
  req.on("end", () => {

    //Parse Data to JSON
    let task = JSON.parse(data);

    //Initiate Order Generation
    (async () => {

      //Log information to console
      console.log("Orders Initiated...")
      console.log("Testing Data: ", data)

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

      //Loop over json object (Array of Dicts) to generate orders based on dict parms
      for (var i = 0; i < task.length; ++i) {

        //Pull Market, Price and Qty
        var m = task[i].market;
        var p = task[i].price;
        var q = task[i].qty;

        //Generate Orders based on Buy vs Sell for Order Module Use (Ease)
        if (task[i].side == "Buy"){

          console.log("Generating Carbon Order...")
          // create an order using Order Module
          // for better input type checking
          const moduleCallResult = await connectedSDK.order.create({
            market: m,
            orderType: OrderModule.OrderType.Limit,
            price: new BigNumber(p),
            quantity: new BigNumber(q),
            side: OrderModule.OrderSide.Buy,
          });
          console.log("Call from Module: \n", moduleCallResult);
        }

        if (task[i].side == "Sell"){

          console.log("Generating Carbon Order...")
          // create an order using Order Module
          // for better input type checking
          const moduleCallResult = await connectedSDK.order.create({
            market: m,
            orderType: OrderModule.OrderType.Limit,
            price: new BigNumber(p),
            quantity: new BigNumber(q),
            side: OrderModule.OrderSide.Sell,
          });
          console.log("Call from Module: \n", moduleCallResult);
        }

      //END LOOP
      }
    //END ASYNC FUNCTION
    });//().catch(console.error).finally(() => process.exit(0));
  //END REQ.ON
  });
//END performTrades
};

export { performTrades };
