import os
from dotenv import load_dotenv
from pybit.unified_trading import HTTP

class Bybit: 
  def __init__(self):
    load_dotenv()
    self.session = HTTP(
      testnet=False, 
      api_key=os.getenv('BYBIT_API_KEY'), 
      api_secret=os.getenv('BYBIT_API_SECRET'),
    )

  def set_leverage(self, symbol, buy_leverage, sell_leverage=None, category="linear"):
    position = self.session.set_leverage(
      category=category,
      symbol=symbol,
      buyLeverage=buy_leverage,
      sellLeverage=sell_leverage
    )
    return position
  
  def set_isolate(self, symbol, buy_leverage, sell_leverage, category="linear"):
    isolate = self.session.switch_margin_mode(
      category=category,
      symbol=symbol,
      buyLeverage=buy_leverage, 
      sellLeverage=sell_leverage
    )
    return isolate

  def place_order(self, symbol, action, order_type, quantity, price, take_profit=None, stop_loss=None, category="linear"):
    order = self.session.place_order(
      category=category,
      symbol=symbol,
      side=action,
      orderType=order_type,
      qty=quantity,
      price=price,
      takeProfit=take_profit,
      stopLoss=stop_loss
    )
    return order
  
  def get_all_balance(self):
    res = ""
    account = self.session.get_coins_balance(accountType="UNIFIED")
    balances = account['result']['balance']
    for balance in balances:
      if balance['walletBalance'] != "0":
        res += f"{balance['coin']}: {balance['walletBalance']}\n"
    return res

