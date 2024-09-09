from telegram import Bot
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

class TelegramNotifier:
    def __init__(self):
        self.bot = Bot(token=TELEGRAM_TOKEN)

    def send_notification(self, message):
        self.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
