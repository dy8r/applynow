from telethon import TelegramClient
import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("TG_API_ID"))
API_HASH = os.getenv("TG_API_HASH")
BOT_TOKEN = os.getenv("TG_BOT_TOKEN")

bot = TelegramClient("job_alert_sender", API_ID, API_HASH).start(bot_token=BOT_TOKEN)


async def send_alert(user_id: int, message: str):
    try:
        await bot.send_message(user_id, message, parse_mode="markdown")
    except Exception as e:
        print(f"Failed to send message to {user_id}: {e}")
