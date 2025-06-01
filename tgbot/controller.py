from typing import List, Tuple
import json
from db_helpers import (
    create_user,
    create_default_alert_if_not_exists,
    get_user_alert_settings,
    get_filter_field,
    get_distinct_companies,
    get_distinct_departments,
    get_distinct_seniorities,
    get_distinct_work_models,
    toggle_boolean_field,
    get_alert_status_flags
)
from telethon import Button

def format_toggle(value: str, selected: bool) -> str:
    display = value.replace("_", " ").title()
    return f"{'✅' if selected else '❌'} {display}"

def create_user_with_alert(user_id: int, username: str):
    create_user(user_id, username)
    create_default_alert_if_not_exists(user_id)

def format_alert_settings_message(user_id: int) -> str:
    settings = get_user_alert_settings(user_id)
    if not settings:
        return "No alert configured."

    lines = ["📢 **Your Job Alert Filters**", "", ""]

    # Alerts status
    if not settings.get("is_active"):
        lines.append("🔕 **ALERTS DISABLED**\n")

    
    # Location
    if settings.get("is_winnipeg"):
        lines.append("📍 **Winnipeg Only**")
    else:
        lines.append("🌎 **All Locations**")

    lines.append("")

    # Salary
    salary_min = settings.get("salary_min")
    salary_max = settings.get("salary_max")
    if salary_min or salary_max:
        lines.append(f"💰 **Salary:** {salary_min or 'Any'} - {salary_max or 'Any'}")
        lines.append("")

    # Multi-value filters
    for field, label in [
        ("work_models", "🏢 **Work Models:**"),
        ("seniorities", "🎓 **Seniorities:**"),
        ("companies", "🏙️ **Companies:**"),
        ("departments", "💼 **Departments:**"),
    ]:
        raw = settings.get(field)
        try:
            parsed = json.loads(raw) if raw else []
        except Exception:
            parsed = []

        if parsed:
            lines.append(f"{label}")
            for val in parsed:
                display_val = val.replace("_", " ").title()
                lines.append(f"\t• {display_val}")
            lines.append("")

    return "\n".join(lines)

def get_filter_buttons(user_id: int, field: str) -> List[Tuple[str, str]]:
    """
    Returns a list of (button_text, callback_data)
    Example: [('✅ Remote', 'toggle:work_models:remote'), ...]
    """
    applied = set(get_filter_field(user_id, field))

    if field == "companies":
        all_options = get_distinct_companies()
    elif field == "departments":
        all_options = get_distinct_departments()
    elif field == "seniorities":
        all_options = get_distinct_seniorities()
    elif field == "work_models":
        all_options = get_distinct_work_models()
    else:
        all_options = []

    return [
        (format_toggle(option, option in applied), f"toggle:{field}:{option}")
        for option in all_options
    ]

def get_applied_filters_text(user_id: int, field: str) -> str:
    """
    Returns a short string like:
    - "All"
    - "• Engineering\n• Design"
    """
    values = get_filter_field(user_id, field)
    if not values:
        return "All"
    return "\n".join(f"\t• {val.replace('_', ' ').title()}" for val in values)

def toggle_is_winnipeg(user_id: int) -> bool:
    """
    Toggle the 'is_winnipeg' boolean and return the new value.
    """
    return toggle_boolean_field(user_id, "is_winnipeg")

def toggle_alert_enabled(user_id: int) -> bool:
    """
    Toggle the 'is_active' boolean and return the new value.
    """
    return toggle_boolean_field(user_id, "is_active")

def is_alert_enabled(user_id: int) -> bool:
    """
    Return whether the current alert is active.
    """
    settings = get_user_alert_settings(user_id)
    return bool(settings.get("is_active")) if settings else False

def is_winnipeg_enabled(user_id: int) -> bool:
    """
    Return whether the alert is set to Winnipeg-only.
    """
    settings = get_user_alert_settings(user_id)
    return bool(settings.get("is_winnipeg")) if settings else False

def get_toggle_buttons(user_id: int):
    flags = get_alert_status_flags(user_id)
    active_label = "🔕 Disable Alerts" if flags.get("is_active") else "🔔 Enable Alerts"
    winnipeg_label = "🌍 All Locations" if not flags.get("is_winnipeg") else "📍 Winnipeg Only"
    return [Button.inline(active_label, b"toggle_alerts")], [Button.inline(winnipeg_label, b"toggle_location")]