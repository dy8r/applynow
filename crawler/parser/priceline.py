import requests
from bs4 import BeautifulSoup, Tag
from ai import enrich_job_posting
from parser import helpers
import time
import random

allowed_departments = [
    "software_engineering",
    "management",
    "design",
    "marketing",
    "sales",
    "hr",
    "finance",
    "support",
    "operations",
    "other"
]

def extract_job_postings():
    url = "https://careers.priceline.com/?s=&post_type=job&_job_location=winnipeg"
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://careers.priceline.com/homepage/winnipeg/",
            "Cache-Control": "no-cache",
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        links = soup.select('a.btn.btn-primary.btn-sm.text-white')

        job_links = []
        for link in links:
            href = link.get("href")
            print("Found job link:", href)
            if href and "careers.priceline.com/job/" in href:
                job_links.append(href)
        visited_links = set()

        for index, job_url in enumerate(job_links):
            try:
                visited_links.add(job_url)

                print(f"🔎 Processing job {index + 1}/{len(job_links)}: {job_url}")

                if helpers.does_job_exist(job_url):
                    print(f"🔴 Job already exists: {job_url}")
                    continue

                result = extract_job_content(job_url)
                if not result:
                    print(f"⚠️ Skipping due to failed content extraction: {job_url}")
                    continue

                title, location, job_type, full_html_description, ai_prompt = result
                if not title or not location or not full_html_description:
                    print(f"⚠️ Skipping due to missing fields: {job_url}")
                    continue


                try:
                    json_data = enrich_job_posting(ai_prompt)
                except Exception as e:
                    print(f"⚠️ AI enrichment failed: {e}")
                    continue

                job_record = {
                    "link": job_url,
                    "title": title,
                    "location": location,
                    "job_type": job_type,
                    "description_html": full_html_description,
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

                if job_record["department"] not in allowed_departments:
                    job_record["department"] = "other"
                    
                print(f"📄 Job record created: {job_record}")

                helpers.upsert_job(job_record, "Priceline")
                print(f"✅ Successfully processed: {title} at {location}")

                time.sleep(random.randint(1, 10))

            except Exception as e:
                print(f"❌ Failed processing job card: {e}")
                continue

        helpers.finalize_crawl("Priceline", job_links)

    except requests.RequestException as e:
        print(f"❌ Failed to fetch initial Priceline page: {e}")


def extract_job_content(url: str):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://careers.priceline.com/?s=&post_type=job&_job_location=winnipeg",
            "Cache-Control": "no-cache",
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract title
        title_tag = soup.find('h1')
        title = title_tag.get_text(strip=True) if title_tag else None

        location = "Winnipeg"
        job_type = "Unknown"

        location, job_type = extract_location_and_type(soup)

        content_container = soup.find('div', class_="entry-content")
        if not content_container:
            print("❌ Couldn't find entry-content container.")
            return None

        content_container = soup.find('div', class_='entry-content')
        if not content_container:
            print("❌ Couldn't find job description container.")
            return None

        formatted_html = extract_description_from_entry_content(content_container)
        ai_prompt = f"{title}\nLocation: {location}\n\n{formatted_html}"

        return title, location, job_type, formatted_html, ai_prompt

    except Exception as e:
        print(f"❌ Failed to parse job details from {url}: {e}")
        return None
    

def extract_description_from_entry_content(entry_content):
    description_parts = []

    for element in entry_content.find_all(['p', 'h2', 'h3', 'h4', 'ul']):
        if element.name in ['h2', 'h3', 'h4']:
            text = element.get_text(strip=True)
            if text:
                description_parts.append(f"<br><strong>{text}</strong><br>")

        elif element.name == 'ul':
            for li in element.find_all('li'):
                bullet = li.get_text(strip=True)
                if bullet:
                    description_parts.append(f"&bull; {bullet}<br>")

        elif element.name == 'p':
            text = element.get_text(strip=True)
            if text:
                description_parts.append(f"{text}<br>")

    return "\n".join(description_parts)


def extract_location_and_type(soup):
    location = "Unknown"
    job_type = "Unknown"

    # Look for a col-12 div that contains both labels
    for div in soup.find_all("div", class_="col-12"):
        tags = div.find_all(['h4', 'p'], recursive=False)
        if any(t.get_text(strip=True).lower() == "location" for t in tags):
            for i in range(len(tags) - 1):
                label = tags[i].get_text(strip=True).lower()
                value = tags[i + 1].get_text(strip=True)

                if label == "location":
                    location = value
                elif label == "career track":
                    job_type = value
            break  # Exit once found

    return location, job_type

