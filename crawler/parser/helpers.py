from typing import List
import database

def does_job_exist(job_link: str) -> bool:
    """
    Check if a job posting already exists in the database.
    """
    if database.does_job_exist(job_link):
        database.update_last_seen(job_link)
        return True
    return False


def upsert_job(job_record: dict, company: str):
    """
    Insert or update a job posting in the database.
    Will automatically set `company`, manage timestamps, and queue notifications.
    """
    job_record["company"] = company

    if database.does_job_exist(job_record["link"]):
        database.update_last_seen(job_record["link"])
    else:
        database.insert_job(job_record)
        database.insert_job_notification_by_link(job_record["link"], event_type="new")


def finalize_crawl(company: str, all_links_found: List[str]):
    """
    After a crawl is complete for a company, mark jobs as archived
    if they were not in the latest scrape and queue archive alerts.
    """
    old_links = database.get_all_links_by_company(company)
    missing_links = [link for link in old_links if link not in all_links_found]

    database.archive_missing_jobs(company, all_links_found)

    for link in missing_links:
        database.insert_job_notification_by_link(link, event_type="archived")
