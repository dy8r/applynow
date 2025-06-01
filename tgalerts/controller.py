from db_helpers import (
    get_pending_job_notifications,
    get_job_by_id,
    get_active_users_with_alerts,
    mark_notifications_sent,
)
from bot import send_alert
import json


def matches_filters(job: dict, alert: dict) -> bool:
    # Winnipeg filter
    if alert.get("is_winnipeg") and not job.get("is_winnipeg"):
        return False

    # JSON filters
    for field in ["departments", "companies", "work_models", "seniorities"]:
        values = alert.get(field)
        if not values:
            continue
        try:
            parsed = json.loads(values)
            if parsed and job.get(field[:-1]) not in parsed:
                return False
        except Exception:
            continue

    return True


def format_job_alert(job: dict) -> str:
    location = job.get("location")
    if not location and job.get("is_winnipeg"):
        location = "Winnipeg"
        
    return (
        f"📢 **New Job Posted!**\n\n"
        f"🏢 **Company**: {job['company']}\n"
        f"💼 **Title**: {job['title']}\n"
        f"📍 **Location:** {location or 'N/A'}\n"
        f"💰 **Salary:** {job.get('salary_min') or 'N/A'} - {job.get('salary_max') or 'N/A'}\n\n"
        f"🔗 [Apply Here]({job['link']})"
    )


async def process_alerts():
    notifications = get_pending_job_notifications()
    if not notifications:
        print("No new job alerts.")
        return

    users = get_active_users_with_alerts()
    sent_jobs = set()

    for notif in notifications:
        job = get_job_by_id(notif["job_id"])
        if not job:
            continue

        for user in users:
            if matches_filters(job, user):
                message = format_job_alert(job)
                try:
                    await send_alert(user["user_id"], message)
                except Exception as e:
                    print(f"Failed to send alert to {user['user_id']}: {e}")
                    continue

                print(f"Sent alert to {user['user_id']} for job {job['id']}")

        sent_jobs.add(job["id"])

    mark_notifications_sent(list(sent_jobs))
    print(f"Marked {len(sent_jobs)} jobs as notified.")
