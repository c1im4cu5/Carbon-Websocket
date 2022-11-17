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

    async def subscribe_market_stats(self, message_id: str):
        """
        Subscribe to market stats.

        Example::

            ws_client.subscribe_market_stats('market_stats')

        The initial channel message is expected as::

            {
                'id':'market_stats',
                'result': ['market_stats']
            }

        The subscription and channel messages are expected as follow::

            {
                'channel': 'market_stats',
                'sequence_number': 484,
                'result': {
                    'cel1_usdc1': {
                        'day_high': '5.97',
                        'day_low': '5.72',
                        'day_open': '5.86',
                        'day_close': '5.74',
                        'day_volume': '414.4',
                        'day_quote_volume': '2429.009',
                        'index_price': '0',
                        'mark_price': '0',
                        'last_price': '5.74',
                        'market': 'cel1_usdc1',
                        'market_type': 'spot',
                        'open_interest': '0'
                    }
                    ...
                }
            }

        :param message_id: Identifier that will be included in the websocket message response to allow the subscriber to
                           identify which channel the notification is originated from.
        :return: None
        """
        channel_name: str = "market_stats"
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

    async def subscribe_positions(self, message_id: str, swth_address: str, market: Optional[str] = None):
        """
        Subscribe to positions channel.

        .. note::
            The market identifier is optional and acts as a filter.

        .. warning::
            This channel is not tested yet.

        :param message_id: Identifier that will be included in the websocket message response to allow the subscriber to
                           identify which channel the notification is originated from.
        :param swth_address: Tradehub wallet address starting with 'swth1' for mainnet and 'tswth1' for testnet.
        :param market: Tradehub market identifier, e.g. 'swth_eth1'
        :return: None
        """
        # TODO not tested yet
        if market:
            channel_name: str = f"positions_by_market:{market}:{swth_address}"
        else:
            channel_name: str = f"positions:{swth_address}"
        await self.subscribe(message_id, [channel_name])

    async def subscribe_recent_trades(self, message_id: str, market: str):
        """
        Subscribe to recent trades.

        Example::

            ws_client.subscribe_recent_trades('trades', "swth_eth1')


        The initial channel message is expected as::

            {
                'id': 'trades',
                'result': ['recent_trades.swth_eth1']
            }

        The channel update messages are expected as::

            {
                'channel': 'recent_trades.eth1_usdc1',
                'sequence_number': 812,
                'result': [
                    {
                        'id': '0',
                        'block_created_at': '2021-02-11T20:49:07.095418551Z',
                        'taker_id': '5FF349410F9CF59BED36D412D1223424835342274BC0E504ED0A17EE4B5B0856',
                        'taker_address': 'swth1vaavrkrm7usqg9hcwhqh2hev9m3nryw7aera8p',
                        'taker_fee_amount': '0.00002',
                        'taker_fee_denom': 'eth1',
                        'taker_side': 'buy',
                        'maker_id': '8334A9C97CAEFAF84774AAADB0D5666E7764BA023DF145C8AF90BB6A6862EA2E',
                        'maker_address': 'swth1wmcj8gmz4tszy5v8c0d9lxnmguqcdkw22275w5',
                        'maker_fee_amount': '-0.00001',
                        'maker_fee_denom': 'eth1',
                        'maker_side': 'sell',
                        'market': 'eth1_usdc1',
                        'price': '1797.1',
                        'quantity': '0.02',
                        'liquidation': '',
                        'taker_username': '',
                        'maker_username': '',
                        'block_height': '7376096'
                    },
                    ...
                ]
            }

        .. warning::
            The field 'id' is sometimes '0'. This endpoint/channel does not seem to work correct.

        :param message_id: Identifier that will be included in the websocket message response to allow the subscriber to
                           identify which channel the notification is originated from.
        :param market: Tradehub market identifier, e.g. 'swth_eth1'
        :return: None
        """
        channel_name: str = f"recent_trades:{market}"
        await self.subscribe(message_id, [channel_name])

    async def subscribe_account_trades(self, message_id: str, swth_address: str, market: Optional[str] = None):
        """
        Subscribe to account trades.

        Example::

            ws_client.subscribe_account_trades('account', 'swth...abcd', 'eth1_usdc1')
            # or for all markets
            ws_client.subscribe_account_trades('account', "swth...abcd')


        The initial channel message is expected as::

            {
                'id': 'account',
                'result': ['account_trades_by_market.eth1_usdc1.swth1...abcd']
            }
            # or for all markets
            {
                'id': 'account',
                'result': ['account_trades.swth1...abcd']
            }

        The channel update messages are expected as::

            {
                'channel': 'recent_trades.eth1_usdc1',
                'sequence_number': 812,
                'result': [
                    {
                        'id': '0',
                        'block_created_at': '2021-02-11T20:49:07.095418551Z',
                        'taker_id': '5FF349410F9CF59BED36D412D1223424835342274BC0E504ED0A17EE4B5B0856',
                        'taker_address': 'swth1...taker',
                        'taker_fee_amount': '0.00002',
                        'taker_fee_denom': 'eth1',
                        'taker_side': 'buy',
                        'maker_id': '8334A9C97CAEFAF84774AAADB0D5666E7764BA023DF145C8AF90BB6A6862EA2E',
                        'maker_address': 'swth1...maker',
                        'maker_fee_amount': '-0.00001',
                        'maker_fee_denom': 'eth1',
                        'maker_side': 'sell',
                        'market': 'eth1_usdc1',
                        'price': '1797.1',
                        'quantity': '0.02',
                        'liquidation': '',
                        'taker_username': '',
                        'maker_username': '',
                        'block_height': '7376096'
                    },
                    ...
                ]
            }

        .. note::
            The market identifier is optional and acts as a filter.

        .. warning::
            The field 'id' is '0' all the time. This endpoint/channel does not seem to work correct.

        :param message_id: Identifier that will be included in the websocket message response to allow the subscriber to
                           identify which channel the notification is originated from.
        :param swth_address: Tradehub wallet address starting with 'swth1' for mainnet and 'tswth1' for testnet.
        :param market: Tradehub market identifier, e.g. 'swth_eth1'
        :return: None
        """
        if market:
            channel_name: str = f"account_trades_by_market:{market}:{swth_address}"
        else:
            channel_name: str = f"account_trades:{swth_address}"
        await self.subscribe(message_id, [channel_name])

    async def subscribe_balances(self, message_id: str, swth_address: str):
        """
        Subscribe to wallet specific balance channel.

        Example::

            ws_client.subscribe_balances('balance', "swth1...abcd')


        The initial channel message is expected as::

            {
                'id': 'balance',
                'result': ['balances.swth1...abcd']
            }

        The subscription and channel messages are expected as follow::

            {
                'channel': 'balances.swth1vaavrkrm7usqg9hcwhqh2hev9m3nryw7aera8p',
                'result': {
                    'eth1': {
                        'available': '0.83941506825',
                        'order': '0',
                        'position': '0',
                        'denom': 'eth1'
                    },
                    ...
                }
            }

        :param message_id: Identifier that will be included in the websocket message response to allow the subscriber to
                           identify which channel the notification is originated from.
        :param swth_address: Tradehub wallet address starting with 'swth1' for mainnet and 'tswth1' for testnet.
        :return: None
        """
        channel_name: str = f"balances:{swth_address}"
        await self.subscribe(message_id, [channel_name])


    async def subscribe_candlesticks(self, message_id: str, market: str, granularity: int):
        """
        Subscribe to candlesticks channel.

        Example::

            ws_client.subscribe_candlesticks('candle', "swth_eth1', 1)


        The initial channel message is expected as::

            {
                'id': 'candle',
                'result': ['candlesticks.swth_eth1.1']
            }

        The subscription and channel messages are expected as follow::

            {
                'channel': 'candlesticks.swth_eth1.1',
                'sequence_number': 57,
                'result': {
                    'id': 0,
                    'market':'swth_eth1',
                    'time': '2021-02-17T10:59:00Z',
                    'resolution': 1,
                    'open': '0.000018',
                    'close': '0.000018',
                    'high': '0.000018',
                    'low': '0.000018',
                    'volume': '5555',
                    'quote_volume': '0.09999'
                }
            }

        :param message_id: Identifier that will be included in the websocket message response to allow the subscriber to
                           identify which channel the notification is originated from.
        :param market: Tradehub market identifier, e.g. 'swth_eth1'
        :param granularity: Define the candlesticks granularity. Allowed values: 1, 5, 15, 30, 60, 360, 1440.
        :return: None
        """
        if granularity not in [1, 5, 15, 30, 60, 360, 1440]:
            raise ValueError(f"Granularity '{granularity}' not supported. Allowed values: 1, 5, 15, 30, 60, 360, 1440")
        channel_name: str = f"candlesticks:{market}:{granularity}"
        await self.subscribe(message_id, [channel_name])

    async def subscribe_commitments(self, message_id: str, swth_address: str) -> dict:

        channel_name: str = f"commitments:{swth_address}"
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
