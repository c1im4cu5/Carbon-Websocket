from typing import Optional, List, Callable
import websockets
import json

class Carbon_Websocket:
    def __init__(self, uri: str, ping_interval: Optional[int] = 10, ping_timeout: Optional[int] = 30):
        self._uri: str = uri
        self._ping_interval: int = ping_interval
        self._ping_timeout: int = ping_timeout

    async def subscribe(self, message_id: str, channels: List[str]):
        await self.send({
            "id": message_id,
            "method": "subscribe",
            "params": {"channels": channels}
        })

    async def subscribe_orders(self, message_id: str, swth_address: str, market: Optional[str] = None):
            if market:
                channel_name: str = f"orders_by_market.{market}.{swth_address}"
            else:
                channel_name: str = f"orders.{swth_address}"
            await self.subscribe(message_id, [channel_name])

    async def send(self, data: dict):
        await self._websocket.send(json.dumps(data))


    def open(self) -> bool:
        if not self._websocket:
            return False

        return self._websocket.open


    async def disconnect(self):
        if self._websocket:
            await self._websocket.close()


    async def connect(self,
        on_receive_message_callback: Callable,
        on_connect_callback: Optional[Callable] = None,
        on_error_callback: Optional[Callable] = None):

        try:
            async with websockets.connect(self._uri,
                                          ping_interval=self._ping_interval,
                                          ping_timeout=self._ping_timeout) as websocket:
                self._websocket = websocket

                if on_connect_callback:
                    await on_connect_callback()

                async for message in websocket:
                    data = json.loads(message)
                    await on_receive_message_callback(data)
        except Exception as e:
            if on_error_callback:
                await on_error_callback(e)
            else:
                raise e
