from telethon import TelegramClient, events, Button
import os
from dotenv import load_dotenv

from controller import (
    create_user_with_alert,
    format_alert_settings_message,
    get_filter_buttons,
    get_applied_filters_text,
    get_toggle_buttons,
    toggle_is_winnipeg, 
    toggle_alert_enabled
)
from db_helpers import toggle_json_field

load_dotenv()

API_ID = int(os.getenv("TG_API_ID"))
API_HASH = os.getenv("TG_API_HASH")
BOT_TOKEN = os.getenv("TG_BOT_TOKEN")

bot = TelegramClient("bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

def filter_buttons(user_id: int, field: str):
    buttons_raw = get_filter_buttons(user_id, field)
    buttons = [[Button.inline(text, data.encode())] for text, data in buttons_raw]
    buttons.append([Button.inline("⬅️ Back", b"back_to_main")])
    return buttons

def filter_handler(field: str, emoji: str, label: str):
    @bot.on(events.CallbackQuery(data=f"edit_{field}".encode()))
    async def show(event):
        user_id = event.sender_id
        buttons = filter_buttons(user_id, field)
        selected = get_applied_filters_text(user_id, field)
        await event.edit(
            f"{emoji} **Select {label.lower()} to get alerts for**\n\n"
            f"**You are receiving notifications for:**\n{selected}",
            buttons=buttons,
            parse_mode="markdown"
        )

    @bot.on(events.CallbackQuery(pattern=f"toggle:{field}:".encode()))
    async def toggle(event):
        user_id = event.sender_id
        val = event.data.decode().split(":")[2]
        toggle_json_field(user_id, field, val)
        buttons = filter_buttons(user_id, field)
        selected = get_applied_filters_text(user_id, field)
        await event.edit(
            f"{emoji} **Select {label.lower()} to get alerts for**\n\n"
            f"**You are receiving notifications for:**\n{selected}",
            buttons=buttons,
            parse_mode="markdown"
        )

filter_handler("departments", "💼", "Departments")
filter_handler("work_models", "🏢", "Work Models")
filter_handler("seniorities", "🎓", "Seniorities")
filter_handler("companies", "🏙️", "Companies")

@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    user = event.sender
    create_user_with_alert(user.id, user.username)
    text = format_alert_settings_message(user.id)

    is_on_button, is_winnipeg_button = get_toggle_buttons(user.id)
    buttons = [
        [Button.inline("💼 Departments", b"edit_departments"), Button.inline("🏢 Work Models", b"edit_work_models")],
        [Button.inline("🎓 Seniorities", b"edit_seniorities"), Button.inline("🏙️ Companies", b"edit_companies")],
        is_winnipeg_button,
        is_on_button,
    ]

    await event.respond(
        text,
        buttons=buttons,
        parse_mode="markdown"
    )

@bot.on(events.CallbackQuery(data=b"back_to_main"))
async def back_to_main(event):
    user_id = event.sender_id
    text = format_alert_settings_message(user_id)
    is_on_button, is_winnipeg_button = get_toggle_buttons(user_id)

    buttons = [
        [Button.inline("💼 Departments", b"edit_departments"), Button.inline("🏢 Work Models", b"edit_work_models")],
        [Button.inline("🎓 Seniorities", b"edit_seniorities"), Button.inline("🏙️ Companies", b"edit_companies")],
        is_winnipeg_button,
        is_on_button,
    ]

    await event.edit(
        text,
        buttons=buttons,
        parse_mode="markdown"
    )

@bot.on(events.CallbackQuery(data=b"toggle_location"))
async def toggle_location(event):
    user_id = event.sender_id
    toggle_is_winnipeg(user_id)

    text = format_alert_settings_message(user_id)
    is_on_button, is_winnipeg_button = get_toggle_buttons(user_id)

    buttons = [
        [Button.inline("💼 Departments", b"edit_departments"), Button.inline("🏢 Work Models", b"edit_work_models")],
        [Button.inline("🎓 Seniorities", b"edit_seniorities"), Button.inline("🏙️ Companies", b"edit_companies")],
        is_winnipeg_button,
        is_on_button,
    ]

    await event.edit(
        text,
        buttons=buttons,
        parse_mode="markdown"
    )


@bot.on(events.CallbackQuery(data=b"toggle_alerts"))
async def toggle_alerts(event):
    user_id = event.sender_id
    toggle_alert_enabled(user_id)

    text = format_alert_settings_message(user_id)
    is_on_button, is_winnipeg_button = get_toggle_buttons(user_id)

    buttons = [
        [Button.inline("💼 Departments", b"edit_departments"), Button.inline("🏢 Work Models", b"edit_work_models")],
        [Button.inline("🎓 Seniorities", b"edit_seniorities"), Button.inline("🏙️ Companies", b"edit_companies")],
        is_winnipeg_button,
        is_on_button,
    ]

    await event.edit(
        text,
        buttons=buttons,
        parse_mode="markdown"
    )

bot.run_until_disconnected()
