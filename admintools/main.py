from telethon import TelegramClient, events
import os
from dotenv import load_dotenv
from db_helpers import get_distinct_ips, get_tg_user_count, get_enabled_alerts_count

load_dotenv()

api_id = int(os.getenv("TG_API_ID"))
api_hash = os.getenv("TG_API_HASH")
bot_token = os.getenv("ADMIN_BOT_TOKEN")
admin_id = int(os.getenv("ADMIN_ID"))

client = TelegramClient("admin_bot_session", api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(pattern="/stats"))
async def stats_handler(event):
    if event.sender_id != admin_id:
        return

    stats = {
        "24h unique users": get_distinct_ips(1),
        "7d unique users": get_distinct_ips(7),
        "30d unique users": get_distinct_ips(30),
        "Telegram users": get_tg_user_count(),
        "Enabled alerts": get_enabled_alerts_count(),
    }

    msg = "\n".join(f"{k}: {v}" for k, v in stats.items())
    await event.respond(f"📊 Stats:\n\n{msg}")

print("Admin bot running...")
client.run_until_disconnected()
