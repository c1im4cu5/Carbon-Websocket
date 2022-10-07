from typing import Optional, List, Callable
import websockets
import json

class Carbon_Websocket:
    def __init__(self, uri: str, ping_interval: Optional[int] = 10, ping_timeout: Optional[int] = 30, close_timeout: Optional[int] = 10):
        self._uri: str = uri
        self._ping_interval: int = ping_interval
        self._ping_timeout: int = ping_timeout
        self._close_timeout: int = close_timeout

    async def subscribe(self, message_id: str, channels: List[str]):
        await self.send({
            "id": message_id,
            "method": "subscribe",
            "params": {"channels": channels}
        })

    async def unsubscribe(self, message_id: str, channels: List[str]):
        await self.send({
            "id": message_id,
            "method": "unsubscribe",
            "params": {"channels": channels}
        })

    async def subscribe_orders(self, message_id: str, swth_address: str, market: Optional[str] = None):
            if market:
                channel_name: str = f"orders_by_market.{market}.{swth_address}"
            else:
                channel_name: str = f"orders.{swth_address}"
            await self.subscribe(message_id, [channel_name])

    async def subscribe_books(self, message_id: str, market: str):
        channel_name: str = f"books:{market}"
        await self.subscribe(message_id, [channel_name])

    async def subscribe_pools(self, message_id: str,  id: Optional[str] = None):
        """
        Expected Return result for this function is as follows:

        {'block_height': 32199893,
        'channel': 'pools',
        'result': {
            '47': {
                'pool': {
                    'creator': 'swth1as3wkrr9mfju4edvpaa8ln44rz9guyacn88888',
                    'id': 47,
                    'name': '50% IBC/A4DB47A9D3CF9A068D454513891B526702455D3EF08FB9EB558C561F9DC2B701 / 50% SWTH Pool',
                    'denom': 'clpt/47', 'denom_a': 'ibc/A4DB47A9D3CF9A068D454513891B526702455D3EF08FB9EB558C561F9DC2B701',
                    'amount_a': '1869222802',
                    'weight_a': '0.500000000000000000',
                    'denom_b': 'swth', 'amount_b': '355396117426371',
                    'weight_b': '0.500000000000000000',
                    'swap_fee': '0.001000000000000000',
                    'num_quotes': 10, 'shares_amount':
                    '812111385717', 'market': 'ATOM_SWTH'
                        },
            'rewards_weight': '4',
            'total_commitment': '1591689895229'
                    }
                    }
        }

        Request get_pools

        .. note::
            The id is optional and acts as a filter.

        .. warning::
            method was tested 5-10-2022

        :param message_id: Identifier that will be included in the websocket message response to allow the subscriber to
                           identify which channel the notification is originated from.
        :param id: Carbon Pool ID
        :return: None
        """
        
        if id:
            channel_name: str = f"pools_by_id:{id}"
        else:
            channel_name: str = f"poools"
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
                                          ping_timeout=self._ping_timeout,
                                          close_timeout=self._close_timeout) as websocket:
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
