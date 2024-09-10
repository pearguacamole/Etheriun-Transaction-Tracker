from telegram.ext import Application
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
from logger import logger

class TelegramNotifier:
    def __init__(self):
        try:
            self.app = Application.builder().token(TELEGRAM_TOKEN).build()
        except Exception as e:
            logger.error(f"Unexpected error with Telegram bot: {e}")

    async def send_notification(self, message):
        try:
            async with self.app:
                await self.app.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        except Exception as e:
            logger.error(f"Unexpected error in Telegram notification: {e}")
