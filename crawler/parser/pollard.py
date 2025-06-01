import requests
from bs4 import BeautifulSoup
from ai import enrich_job_posting
from parser import helpers
import time
import random

BASE_URL = "https://www.pollardbanknote.com/technology-digital/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
}


def extract_job_postings():
    try:
        response = requests.get(BASE_URL, headers=HEADERS, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        job_links = []

        visited_links = set()
        job_titles = soup.find_all("h3", class_="elementor-post__title")

        for index, title in enumerate(job_titles):
            try:
                a_tag = title.find("a")
                if not a_tag or not a_tag.get("href"):
                    continue

                link = a_tag["href"]
                if link in visited_links:
                    continue
                visited_links.add(link)

                print(f"🔎 Processing job {index + 1}: {link}")

                if helpers.does_job_exist(link):
                    print(f"🔴 Job already exists: {link}")
                    continue

                result = extract_job_content(link)
                if not result:
                    print(f"⚠️ Skipping: Failed to extract job content: {link}")
                    continue

                title, location, job_type, description_html, ai_prompt = result
                if not title or not location or not description_html:
                    print(f"⚠️ Skipping: Missing fields for {link}")
                    continue

                try:
                    json_data = enrich_job_posting(ai_prompt)
                except Exception as e:
                    print(f"⚠️ AI enrichment failed: {e}")
                    continue

                job_record = {
                    "link": link,
                    "title": title,
                    "location": None, # They specify location directly in the description. Hard to parse.
                    "job_type": None,
                    "description_html": description_html,
                    "salary_min": json_data.get("salary_min"),
                    "salary_max": json_data.get("salary_max"),
                    "work_model": json_data.get("work_model"),
                    "industry": json_data.get("industry"),
                    "seniority": json_data.get("seniority"),
                    "technologies": json_data.get("technologies"),
                    "is_winnipeg": json_data.get("is_winnipeg"),
                    "department": json_data.get("department"),
                    "min_experience": json_data.get("min_experience"),
                }

                helpers.upsert_job(job_record, "Pollard")
                print(f"✅ Inserted: {title} at {location}")

                time.sleep(random.randint(1, 6))

            except Exception as e:
                print(f"❌ Failed processing job link: {e}")
                continue


    except requests.RequestException as e:
        print(f"❌ Failed to fetch Pollard careers page: {e}")


def extract_job_content(url: str):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        title_tag = soup.find("h2", class_="vidcruiter-job-item-title")
        title = title_tag.get_text(strip=True) if title_tag else "Untitled"

        content_div = soup.find("div", class_="vidcruiter-job-board-individual-container")
        if not content_div:
            print(f"❌ Could not find job container for: {url}")
            return None

        # Extract HTML description
        description_html = content_div.decode_contents()

        # Try to infer location and job type (use AI if necessary)
        location = "Unknown"
        job_type = "Unknown"

        ai_prompt = f"{title}\nLocation: {location}\nType: {job_type}\n\n{description_html}"

        return title, location, job_type, description_html, ai_prompt

    except Exception as e:
        print(f"❌ Failed to parse job details from {url}: {e}")
        return None
