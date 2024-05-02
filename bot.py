import os
import logging
import process
from dotenv import load_dotenv
from Bybit import Bybit
from BinanceAPI import BinanceAPI
from telethon.sync import TelegramClient, events
# from telegram.ext import Updater, CommandHandler, MessageHandler
# from telethon.tl.types import PeerChannel
load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
SESSION_NAME = os.getenv('SESSION_NAME')
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

setting = {
    'cex': 'bybit',
    'order_amt': 10,
    'tp_pct': 0.1,
    'stl_pct': 0.05
}

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

bybit = Bybit()
bAPI = BinanceAPI()

# def settings(update, context):
#     response = ""
#     if not isAdmin(update.message.from_user.username):
#         return
#     try:
#         params = context.args
#         if len(params) != 4:
#             response = "Invalid parameters. \nUsage: /setting <cex: bybit/binance> <place_amount> <default_tp_%> <default_stl_%>"
#             update.message.reply_text(response)
#         setting['cex'] = params[0]
#         setting['order_amt'] = params[1]
#         setting['tp_pct'] = params[2]
#         setting['tl_pct'] = params[3]
#         response = "Settings updated successfully."
#         update.message.reply_text(response)
#     except (IndexError, ValueError):
#         response = "Invalid parameters. \nUsage: /setting <cex: bybit/binance> <place_amount> <default_tp_%> <default_stl_%>"
#         update.message.reply_text(response)

# def balances(update, context):
    response = ""
    if not isAdmin(update.message.from_user.username):
        return
    try: 
        params = context.args
        if len(params) != 0:
            response = "Invalid parameters.\nUsage: /MB"
            update.message.reply_text(response) 
            return
    except (IndexError, ValueError):
        response = "Invalid parameters.\nUsage: /MB"
        update.message.reply_text(response)

    try:
        if setting['cex'] == 'binance':
            response = bAPI.get_all_balance()
        else:
            response = bybit.get_all_balance()
        update.message.reply_text(response) 
    except Exception as e:
        response = f"Failed to get my balance: {e}"
        update.message.reply_text(response) 

# def help(update, context):
#     if not isAdmin(update.message.from_user.username):
#         return
#     update.message.reply_text(helpMessage)

# def isAdmin(username):
#     return username == 'cgccld'

# def error_handler(update, context):
#     """Log any errors that occur."""
#     logger.error(f"Update {update} caused error {context.error}")

def main():
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    @client.on(events.NewMessage(chats=[CHANNEL_ID]))
    async def handler(event):
        print(event.raw_text)
        processedData = process.preprocess_msg(event.raw_text, setting=setting)
        if processedData['entry'] != None and processedData['token'] != None:
            order = bybit.place_order(
                symbol=processedData['token'],
                action=processedData['action'].capitalize(),
                order_type="Limit",
                price=processedData['entry'],
                take_profit=str(round(processedData['tp'], 4)),
                stop_loss=str(round(processedData['stl'], 4)),
                quantity=str(int(float(setting['order_amt']) / float(processedData['entry'])))
            )
            print(order)
            leverage = bybit.set_leverage(
                symbol=processedData['token'],
                buy_leverage=processedData['buyLeverage'],
                sell_leverage=processedData['sellLeverage']
            )
            print(leverage)
            isolated = bybit.set_isolate(
                symbol=processedData['token'],
                buy_leverage=processedData['buyLeverage'],
                sell_leverage=processedData['sellLeverage']
            )
            print(isolated)
    client.start()
    client.run_until_disconnected()

if __name__ == '__main__':
    main()
