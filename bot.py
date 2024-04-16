import os
import logging
from dotenv import load_dotenv
from BinanceAPI import BinanceAPI
from telegram.ext import Updater, CommandHandler

load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

bAPI = BinanceAPI() 

helpMessage = '''
/BM - Buy Market
/SM - Sell Market
/BL - Buy Limit
/SL - Sell Limit
/OO - Open Orders
/MPof - Market Price
/CO - Cancel Order
/MB - My balance
'''

def buy_market(update, context):
    response = ""
    if not isAdmin(update.message.from_user.username):
        return
    try: 
        params = context.args
        if len(params) != 2:
            response = "Invalid parameters.\nUsage: /BM <market> <quantity>"
            update.message.reply_text(response)
            return
        market = params[0]
        quantity = params[1]
    except (IndexError, ValueError):
        response = "Invalid parameters.\nUsage: /BM <market> <quantity>"
        update.message.reply_text(response)
    try: 
        response = bAPI.buy_market(market=market, quantity=quantity)
        update.message.reply_text(response)
    except Exception as e:
        response = f"Failed to buy market: {e}"
        update.message.reply_text(response)

def sell_market(update, context):
    response = ""
    if not isAdmin(update.message.from_user.username):
        return
    try: 
        params = context.args
        if len(params) != 2:
            response = "Invalid parameters.\nUsage: /SM <market> <quantity>"
            update.message.reply_text(response) 
            return
        market = params[0]
        quantity = params[1]
    except (IndexError, ValueError):
        response = "Invalid parameters.\nUsage: /SM <market> <quantity>"
        update.message.reply_text(response) 
    try: 
        response = bAPI.sell_market(market=market, quantity=quantity)
        update.message.reply_text(response) 
    except Exception as e:
        response = f"Failed to sell market: {e}"
        update.message.reply_text(response) 

def buy_limit(update, context):
    response = ""
    if not isAdmin(update.message.from_user.username):
        return
    try: 
        params = context.args
        if len(params) != 3:
            response = "Invalid parameters.\nUsage: /BL <market> <quantity> <rate>"
            update.message.reply_text(response) 
            return
        market = params[0]
        quantity = params[1]
        rate = params[2]
    except (IndexError, ValueError):
        response = "Invalid parameters.\nUsage: /BL <market> <quantity> <rate>"
        update.message.reply_text(response) 
    try: 
        response = bAPI.buy_limit(market=market, quantity=quantity, rate=rate)
        update.message.reply_text(response) 
    except Exception as e:
        response = f"Failed to buy limit: {e}"
        update.message.reply_text(response)

def sell_limit(update, context):
    response = ""
    if not isAdmin(update.message.from_user.username):
        return
    try: 
        params = context.args
        if len(params) != 3:
            response = "Invalid parameters.\nUsage: /SL <market> <quantity> <rate>"
            update.message.reply_text(response) 
            return
        market = params[0]
        quantity = params[1]
        rate = params[2]
    except (IndexError, ValueError):
        response = "Invalid parameters.\nUsage: /SL <market> <quantity> <rate>"
        update.message.reply_text(response) 
    try: 
        response = bAPI.sell_limit(market=market, quantity=quantity, rate=rate)
        update.message.reply_text(response) 
    except Exception as e:
        response = f"Failed to sell limit: {e}"
        update.message.reply_text(response) 

def cancel_order(update, context):
    response = ""
    if not isAdmin(update.message.from_user.username):
        return
    try: 
        params = context.args
        if len(params) != 2:
            response = "Invalid parameters.\nUsage: /CO <market> <orderId>"
            update.message.reply_text(response) 
            return
        market = params[0]
        orderId = params[1]
    except (IndexError, ValueError):
        response = "Invalid parameters.\nUsage: /CO <market> <orderId>"
        update.message.reply_text(response) 
    try: 
        response = bAPI.cancel_order(market=market, orderId=orderId)
        update.message.reply_text(response) 
    except Exception as e:
        response = f"Failed to cancel order: {e}"
        update.message.reply_text(response)

def get_market_price(update, context):
    response = ""
    if not isAdmin(update.message.from_user.username):
        return
    try: 
        params = context.args
        if len(params) != 1:
            response = "Invalid parameters.\nUsage: /MPof <market>"
            update.message.reply_text(response) 
            return
        market = params[0]
    except (IndexError, ValueError):
        response = "Invalid parameters.\nUsage: /MPof <market>"
        update.message.reply_text(response) 
    try: 
        response = bAPI.get_market_price(market=market)
        update.message.reply_text(response) 
    except Exception as e:
        response = f"Failed to get market order: {e}"
        update.message.reply_text(response) 

def get_open_orders(update, context):
    response = ""
    if not isAdmin(update.message.from_user.username):
        return
    try: 
        params = context.args
        if len(params) != 1:
            response = "Invalid parameters.\nUsage: /OO <market>"
            update.message.reply_text(response) 
            return
        market = params[0]
    except (IndexError, ValueError):
        response = "Invalid parameters.\nUsage: /OO <market>"
        update.message.reply_text(response) 
    try: 
        response = bAPI.get_open_orders(market=market)
        update.message.reply_text(response) 
    except Exception as e:
        response = f"Failed to get open order: {e}"
        update.message.reply_text(response)  

def get_my_balance(update, context):
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
        response = bAPI.get_all_balance()
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

    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("BM", buy_market))
    dispatcher.add_handler(CommandHandler("SM", sell_market))
    dispatcher.add_handler(CommandHandler("BL", buy_limit))
    dispatcher.add_handler(CommandHandler("SL", sell_limit))
    dispatcher.add_handler(CommandHandler("CO", cancel_order))
    dispatcher.add_handler(CommandHandler("OO", get_open_orders))
    dispatcher.add_handler(CommandHandler("MPof", get_market_price))
    dispatcher.add_handler(CommandHandler("MB", get_my_balance))

    dispatcher.add_error_handler(error_handler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
