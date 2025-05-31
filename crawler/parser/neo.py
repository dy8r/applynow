import requests
from bs4 import BeautifulSoup
from ai import enrich_job_posting
from parser import helpers
import time
import random

base_url = "https://ats.rippling.com"

def extract_job_postings():
    org_path = "/neo-financial/jobs"
    page = 0
    all_job_links = set()

    while True:
        page_url = f"{base_url}{org_path}?page={page}"
        print(f"Fetching page {page}: {page_url}")

        try:
            response = requests.get(page_url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            found_links = 0

            for a_tag in soup.find_all('a', href=True):
                button = a_tag.find('button', attrs={"data-testid": "Apply"})
                if button:
                    full_link = base_url + a_tag['href']
                    if full_link not in all_job_links:
                        all_job_links.add(full_link)
                        print(f"🟢 Found job: {full_link}")
                        found_links += 1

            if found_links == 0:
                print(f"🔚 No jobs found on page {page}. Ending.")
                break

            page += 1

        except requests.RequestException as e:
            print(f"❌ Request failed on page {page}: {e}")
            break

    print(f"\n✅ Total jobs found: {len(all_job_links)}")
    all_job_links = list(all_job_links)
    jobs_length = len(all_job_links)

    for index, job_link in enumerate(all_job_links):
        print(f"🔗 Processing job {index + 1}/{jobs_length}: {job_link}")
        try:
            print(f"\n🔍 Processing job: {job_link}")
            does_job_exist = helpers.does_job_exist(job_link)
            if does_job_exist:
                print(f"🔴 Job already exists: {job_link}")
                continue
            title, location, department, full_description, html_block, ai_prompt = extract_job_content(job_link)

            if not title or not location or not html_block:
                print(f"❌ Skipping job due to missing data: {job_link}")
                continue

            try:
                json_data = enrich_job_posting(ai_prompt)
            except Exception as e:
                print(f"⚠️ AI enrichment failed for {job_link}: {e}")
                continue

            # Unpack AI-enriched data safely
            try:
                job_record = {
                    "link": job_link,
                    "title": title,
                    "location": location,
                    "job_type": department or "Unknown",
                    "description_html": str(full_description),
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

                helpers.upsert_job(job_record, "Neo")
                print(f"✅ Successfully processed job: {title} at {location}")

                sleep_time = random.randint(1, 5)
                print(f"⏱️ Sleeping for {sleep_time} seconds...")
                time.sleep(sleep_time)

            except Exception as e:
                print(f"❌ Failed to build/save job record for {job_link}: {e}")
                continue

        except Exception as e:
            print(f"❌ Unexpected error processing job {job_link}: {e}")
            continue

    helpers.finalize_crawl("Neo", all_job_links)


def extract_job_content(job_url: str):
    try:
        response = requests.get(job_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # 1. Title from <h2>
        title_tag = soup.find('h2')
        title = title_tag.get_text(strip=True) if title_tag else None

        # 2. Location
        location = None
        icon_span = soup.find('span', attrs={"data-icon": "LOCATION_OUTLINE"})
        if icon_span:
            parent = icon_span.find_parent()
            location_p = parent.find_next('p') if parent else None
            if location_p:
                location = location_p.get_text(strip=True)

        # 3. Department
        department = None
        icon_span = soup.find('span', attrs={"data-icon": "DEPARTMENTS_OUTLINE"})
        if icon_span:
            parent = icon_span.find_parent()
            department_p = parent.find_next('p') if parent else None
            if department_p:
                department = department_p.get_text(strip=True)

        # 4. Job description container
        html_block = soup.find('div', class_='ATS_htmlPreview')
        if not html_block:
            ai_prompt = f"Job Title: {title}\nJob Location: {location}\n"
            print(f"❌ No job content div for {job_url}")
            return title, location, department, None, None, ai_prompt

        # 5. Extract and format paragraphs and list items
        description_parts = []

        for child in html_block.children:
            if isinstance(child, str):
                continue

            if child.name == 'p':
                text = child.get_text(strip=True)
                if text:
                    description_parts.append(f"<p>{text}</p>")

            elif child.name == 'ul':
                for li in child.find_all('li'):
                    bullet_text = li.get_text(strip=True)
                    if bullet_text:
                        description_parts.append(f"<p>&bull; {bullet_text}</p>")

            elif child.name == 'div':
                for subchild in child.children:
                    if getattr(subchild, 'name', None) == 'p':
                        text = subchild.get_text(strip=True)
                        if text:
                            description_parts.append(f"<p>{text}</p>")
                    elif subchild.name == 'ul':
                        for li in subchild.find_all('li'):
                            bullet_text = li.get_text(strip=True)
                            if bullet_text:
                                description_parts.append(f"<p>&bull; {bullet_text}</p>")

        full_description = "\n".join(description_parts)

        ai_prompt = f"""
Job Title: {title}
Job Location: {location}
Job Description:
{BeautifulSoup(full_description, 'html.parser').get_text()}
""".strip()

        return title, location, department, full_description, html_block, ai_prompt

    except requests.RequestException as e:
        print(f"❌ Failed to fetch job content from {job_url}: {e}")
        return None, None, None, None, None, None
    except Exception as e:
        print(f"⚠️ Unexpected parsing error at {job_url}: {e}")
        return None, None, None, None, None, None