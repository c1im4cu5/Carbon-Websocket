import { BigNumber } from "bignumber.js";
import * as BIP39 from "bip39";
import { OrderModule } from "../lib";
import { MsgCreateOrder } from "../lib/codec/order/tx";
import { CarbonTx } from "../lib/util";
import { CarbonSDK } from "./_sdk";
import "./_setup";
import data from '../orders.json';

var path = require('path');
var rootDirname = path.basename(path.dirname("orders.json")); // the parent of the root path

(async () => {

  console.log("Orders Initiated...")
  console.log("Testing Data: ", data)

  const mnemonics = process.env.MNEMONICS ?? BIP39.generateMnemonic();
  console.log("Mnemonic: ", mnemonics);

  const sdk = await CarbonSDK.instance({
    network: CarbonSDK.Network.MainNet,
    /*config: {
      tmRpcUrl: process.env.TRPC_ENDPOINT,
    },*/
  });
  const connectedSDK = await sdk.connectWithMnemonic(mnemonics);
  console.log("Carbon SDK Connected");

  for (var i = 0; i < data.length; ++i) {
    var m = data[i].market;
    var p = data[i].price;
    var q = data[i].qty;

    console.log("Price: ", p);
    console.log("Qty: ", q);

    if (data[i].side == "Buy"){

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

    if (data[i].side == "Sell"){

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

    delete data[i];
  }

  var filtered = data.filter(function (el) {
    return el != null;
  });

  var fs = require('fs');
  var f = rootDirname + "/orders.json"

  fs.writeFileSync(f, JSON.stringify(filtered), 'utf8', function(err: String) {
    if (err) {
              return console.error(err);
              }
    console.log("File created!");
  });

})().catch(console.error).finally(() => process.exit(0));
