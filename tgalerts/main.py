import asyncio
import time
from controller import process_alerts
from bot import bot

POLL_INTERVAL = 30  # seconds

async def main_loop():
    while True:
        try:
            print("🔍 Checking for new alerts...")
            await process_alerts()
            print("✅ Alerts processed successfully.")
        except Exception as e:
            print(f"❌ Error processing alerts: {e}")
        print(f"⏳ Waiting for {POLL_INTERVAL} seconds before next check...")
        await asyncio.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    with bot:
        bot.loop.run_until_complete(main_loop())
