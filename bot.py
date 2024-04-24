import os
import logging
import process
from dotenv import load_dotenv
from Bybit import Bybit
from BinanceAPI import BinanceAPI
from telethon.sync import TelegramClient, events
from telegram.ext import Updater, CommandHandler
from telethon.tl.types import PeerChannel
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

helpMessage = '''
/setting
/balances
'''
def settings(update, context):
    response = ""
    if not isAdmin(update.message.from_user.username):
        return
    try:
        params = context.args
        if len(params) != 4:
            response = "Invalid parameters. \nUsage: /setting <cex: bybit/binance> <place_amount> <default_tp_%> <default_stl_%>"
            update.message.reply_text(response)
        setting['cex'] = params[0]
        setting['order_amt'] = params[1]
        setting['tp_pct'] = params[2]
        setting['tl_pct'] = params[3]
        response = "Settings updated successfully."
        update.message.reply_text(response)
    except (IndexError, ValueError):
        response = "Invalid parameters. \nUsage: /setting <cex: bybit/binance> <place_amount> <default_tp_%> <default_stl_%>"
        update.message.reply_text(response)

def balances(update, context):
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

def help(update, context):
    if not isAdmin(update.message.from_user.username):
        return
    update.message.reply_text(helpMessage)

def isAdmin(username):
    return username == 'cgccld'

def error_handler(update, context):
    """Log any errors that occur."""
    logger.error(f"Update {update} caused error {context.error}")

def main():
    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher
    
    # dispatcher.add_handler(CommandHandler("balances", balances))s
    # dispatcher.add_handler(CommandHandler("settings", settings))
    # dispatcher.add_error_handler(error_handler)
    # updater.start_polling()
    # updater.idle()

    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    channels = [CHANNEL_ID]
    @client.on(events.NewMessage(chats=[CHANNEL_ID]))
    async def handler(event):
        print(event.raw_text)
        processedData = process.preprocess_msg(event.raw_text, setting=setting)
        if processedData['entry'] != None and processedData['token'] != None:
            position = bybit.set_leverage(
                symbol=processedData['token'],
                
                buy_leverage="10",
                sell_leverage="10",
            )
            print(position)
            updater.message.reply_text(f"Set leverage {processedData['token']} succeeded")
            order = bybit.place_order(
                symbol=processedData['token'],
                action=processedData['action'].capitalize(),
                order_type="Limit",
                price=processedData['entry'],
                take_profit=processedData['tp'],
                stop_loss=processedData['stl'],
                quantity=str((float(setting['order_amt']) * 10) / float(processedData['entry']))
            )
            print(order)
            updater.message.reply_text(f"{processedData['action']} {processedData['token']} at {processedData['entry']} succeeded")
    client.start()
    client.run_until_disconnected()
    # messages = client.get_messages(PeerChannel(channel_id=CHANNEL_ID))
    # for message in client.iter_messages(PeerChannel(channel_id=CHANNEL_ID)):
    #     try:
    #         processedData = process.preprocess_msg(message.text, setting)
    #         print(processedData)
    #         if processedData['entry'] is not None and processedData['token'] is not None:
    #             print("aaaa")
    #             position = bybit.set_leverage(
    #                 symbol=processedData['token'],
    #                 buy_leverage="10",
    #                 sell_leverage="10",
    #             )
    #             print(position)
    #             action = processedData['action'].capitalize()
    #             quantity = str(setting['order_amt'] * 10 / float(processedData['entry']))
    #             order = bybit.place_order(
    #                 symbol=processedData['token'],
    #                 action=action,
    #                 ordstrtype="Limit",
    #                 price=processedData['entry'],
    #                 take_profit=processedData['tp'],
    #                 stop_loss=processedData['stl'],
    #                 isLeverage=1,
    #                 quantity=quantity
    #             )
    #             print(order)
    #     except Exception as e:
    #         print(e)

if __name__ == '__main__':
    main()
