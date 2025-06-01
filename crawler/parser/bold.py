import requests
import time
import random
from ai import enrich_job_posting
from parser import helpers

BASE_LIST_URL = "https://boldcommerce.bamboohr.com/careers/list"
DETAIL_URL_TEMPLATE = "https://boldcommerce.bamboohr.com/careers/{}/detail"

def extract_job_postings():
    try:
        resp = requests.get(BASE_LIST_URL, timeout=10)
        resp.raise_for_status()
        jobs = resp.json()["result"]
        all_links = set()

        for job in jobs:
            job_id = job["id"]
            print(f"📄 Processing job ID: {job_id}")
            job_data = fetch_job_detail(job_id)
            if not job_data:
                continue

            job_opening = job_data["jobOpening"]
            title = job_opening["jobOpeningName"]
            location = job_opening.get("atsLocation", {}).get("city") or "Unknown"
            state = job_opening.get("atsLocation", {}).get("state")
            job_type = job_opening.get("employmentStatusLabel", "Unknown")
            description_html = job_opening.get("description", "")
            link = job_opening.get("jobOpeningShareUrl")
            date_posted = job_opening.get("datePosted")

            if helpers.does_job_exist(link):
                print(f"🔴 Already exists: {link}")
                continue

            is_winnipeg = "winnipeg" in (location or "").lower() or "winnipeg" in description_html.lower()

            ai_prompt = f"{title}\nLocation: {location}\nType: {job_type}\n\n{description_html}"
            try:
                json_data = enrich_job_posting(ai_prompt)
            except Exception as e:
                print(f"⚠️ AI enrichment failed: {e}")
                continue

            job_record = {
                "link": link,
                "title": title,
                "location": location,
                "job_type": job_type,
                "description_html": description_html,
                "salary_min": json_data.get("salary_min"),
                "salary_max": json_data.get("salary_max"),
                "work_model": json_data.get("work_model"),
                "industry": json_data.get("industry"),
                "seniority": json_data.get("seniority"),
                "technologies": json_data.get("technologies"),
                "is_winnipeg": is_winnipeg,
                "department": json_data.get("department") or "other",
                "min_experience": json_data.get("min_experience"),
            }


            helpers.upsert_job(job_record, "Bold")
            all_links.add(link)
            print(f"✅ Upserted job: {title} at {location}")

            time.sleep(random.randint(1, 5))

        all_links_found = list(all_links)
        helpers.finalize_crawl("Bold", all_links_found)

    except Exception as e:
        print(f"❌ Failed to process Bold jobs: {e}")

def fetch_job_detail(job_id):
    try:
        url = DETAIL_URL_TEMPLATE.format(job_id)
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.json()["result"]
    except Exception as e:
        print(f"❌ Failed to fetch job {job_id}: {e}")
        return None
