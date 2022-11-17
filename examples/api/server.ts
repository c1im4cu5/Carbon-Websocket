import * as http from "http";

// import controller
import { performTrades } from "./examples/create_orders";

// create the http server
const server = http.createServer((req, res) => {

      // get tasks
  if (req.method == "GET" && req.url == "/trading") {
    return getTasks(req, res);
  }

  // Post request to perform trades
  if (req.method == "POST" && req.url == "/trade") {
    performTrades(req, res);
  }
});

// set up the server port and listen for connections
server.listen(3000, () => {
   console.log("Server is running on port 3000");
});
