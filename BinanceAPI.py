import os
from binance.enums import *
from dotenv import load_dotenv
from binance.client import Client

class BinanceAPI:
    def __init__(self):
        load_dotenv()
        BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
        BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET')
        self.client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)

    def get_open_orders(self, market):
        order = self.client.get_open_orders(symbol=market)
        return order

    def cancel_order(self, market, orderID):
        order = self.client.cancel_order(
            symbol=market,
            orderId=orderID)
        return order

    def get_balance(self, market="BTC"):
        balance = self.client.get_asset_balance(asset=market)
        balance = balance['free']
        return balance
    
    def get_all_balance(self):
        res = ""
        account = self.client.get_account()
        balances = account['balances']
        non_zero_balances = [balance for balance in balances if float(balance['free']) > 0]
        for balance in non_zero_balances:
            res += f"{balance['asset']}: {balance['free']}\n"
        return res

    def get_market_price(self, market):
        depth = self.client.get_order_book(symbol=market, limit=5)
        lastBid = float(depth['bids'][0][0]) #last buy price (bid)
        lastAsk = float(depth['asks'][0][0]) #last sell price (ask)
        return lastBid, lastAsk

    def buy_market(self, market, quantity):
        order = self.client.order_market_buy(
            symbol=market,
            quantity=quantity)    
        return order

    def sell_market(self, market, quantity):
        order = self.client.order_market_sell(
            symbol=market,
            quantity=quantity)    
        return order

    def buy_limit(self, market, quantity, rate):
        order = self.client.order_limit_buy(
            symbol=market,
            quantity=quantity,
            price=rate)    
        return order

    def sell_limit(self, market, quantity, rate):
        order = self.client.order_limit_sell(
            symbol=market,
            quantity=quantity,
            price=rate)    
        return order
