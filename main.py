import os
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Telegram Bot API Token
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

# Vehicle Info API Key
API_KEY = 'ce27f90472f3654e56d8ccf9a9cc7aa4'
API_URL = 'https://api.cyberethic.in/vehicle.php'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome! Send a vehicle number to get its information.')

def vehicle_info(update: Update, context: CallbackContext) -> None:
    vehicle_number = update.message.text
    url = f'{API_URL}?key={API_KEY}&number={vehicle_number}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['statusCode'] == 200:
            vehicle_data = data['response']
            info = f"*Vehicle Information*\n"
            info += f"*Registration Number:* {vehicle_data['regNo']}\n"
            info += f"*RTO Code:* {vehicle_data['rtoCode']}\n"
            info += f"*Registration Authority:* {vehicle_data['regAuthority']}\n"
            info += f"*Chassis Number:* {vehicle_data['chassis']}\n"
            info += f"*Engine Number:* {vehicle_data['engine']}\n"
            info += f"*Registration Date:* {vehicle_data['regDate']}\n"
            info += f"*Vehicle Class:* {vehicle_data['vehicleClass']}\n"
            info += f"*PUCC Number:* {vehicle_data['puccNumber']}\n"
            info += f"*PUCC Valid Upto:* {vehicle_data['puccValidUpto']}\n"
            info += f"*Owner:* {vehicle_data['owner']}\n"
            info += f"*Insurance Company:* {vehicle_data['insuranceCompanyName']}\n"
            info += f"*Insurance Valid Upto:* {vehicle_data['insuranceUpto']}\n"
            update.message.reply_text(info, parse_mode='Markdown')
        else:
            update.message.reply_text('Failed to retrieve vehicle information.')
    else:
        update.message.reply_text('Failed to retrieve vehicle information.')

def main() -> None:
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, vehicle_info))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
