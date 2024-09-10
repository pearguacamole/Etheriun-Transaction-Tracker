from telegram import Bot
from telegram.ext import Application
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID


class TelegramNotifier:
    def __init__(self):
        self.app = Application.builder().token(TELEGRAM_TOKEN).build()

    async def send_notification(self, message):
        async with self.app:
            await self.app.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
