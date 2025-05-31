import requests
from bs4 import BeautifulSoup
from ai import enrich_job_posting
from parser import helpers
import time
import random

def extract_job_postings():
    url = "https://payworksinc.easyapply.co/"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        job_cards = soup.find_all('a', class_='job_apply_link')
        job_links = []
        visited_links = set()

        for index, job in enumerate(job_cards):
            try:
                print(f"Processing job {index + 1}/{len(job_cards)}: {job.get_text(strip=True)}")
                link = job['href']
                if link in visited_links:
                    continue
                visited_links.add(link)

                actual_job_link = resolve_actual_job_link(link)
                if not actual_job_link:
                    print("⚠️ Failed to resolve actual job link.")
                    continue

                job_links.append(actual_job_link)
                try:
                    does_job_exist = helpers.does_job_exist(actual_job_link)
                    if does_job_exist:
                        print(f"🔴 Job already exists: {actual_job_link}")
                        continue
                    result = extract_job_content(actual_job_link)
                    if not result:
                        print(f"⚠️ Skipping due to failed content extraction: {actual_job_link}")
                        continue

                    title, location, job_type, full_html_description, ai_prompt = result
                    if not title or not location or not full_html_description:
                        print(f"⚠️ Skipping due to missing fields: {actual_job_link}")
                        continue

                    try:
                        json_data = enrich_job_posting(ai_prompt)
                    except Exception as e:
                        print(f"⚠️ AI enrichment failed: {e}")
                        continue

                    job_record = {
                        "link": actual_job_link,
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

                    helpers.upsert_job(job_record, "Payworks")
                    print(f"✅ Successfully processed job: {title} at {location}")

                    sleep_time = random.randint(1, 10)
                    print(f"⏱️ Sleeping {sleep_time}s to be kind to the server...")
                    time.sleep(sleep_time)

                except Exception as e:
                    print(f"❌ Unexpected failure processing job {actual_job_link}: {e}")
                    continue

            except Exception as e:
                print(f"❌ Failed to process a job card: {e}")
                continue

        helpers.finalize_crawl("Payworks", job_links)

    except requests.RequestException as e:
        print(f"❌ Initial page request failed: {e}")


def resolve_actual_job_link(slug_url: str) -> str:
    try:
        response = requests.get(slug_url, allow_redirects=False, timeout=10)
        if response.status_code == 302:
            return "https://easyapply.co" + response.headers.get('Location')
        else:
            print(f"⚠️ Unexpected status code {response.status_code} for URL: {slug_url}")
            return None
    except requests.RequestException as e:
        print(f"❌ Request failed for {slug_url}: {e}")
        return None


def extract_job_content(actual_url: str):
    try:
        response = requests.get(actual_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        main_col = soup.find('div', class_='col-lg-7')
        if not main_col:
            print("❌ Couldn't find job content column.")
            return None

        # Title
        title_tag = main_col.find('h1')
        title = title_tag.get_text(strip=True) if title_tag else None

        # Location
        location_span = main_col.find('i', class_='icon-map-marker')
        location = location_span.find_parent('span').get_text(strip=True) if location_span else None

        # Job Type
        type_span = main_col.find('i', class_='fa fa-clock-o')
        job_type = type_span.find_parent('span').get_text(strip=True) if type_span else None

        # Description container
        content_container = main_col.find('div', attrs={"test-id": True})
        if not content_container:
            print("❌ Couldn't find job description container.")
            return None

        description_parts = []

        for child in content_container.children:
            if isinstance(child, str):
                continue

            if child.name == 'p':
                text = child.get_text(strip=True)
                if text:
                    description_parts.append(f"<p>{text}</p>")

            elif child.name == 'ul':
                for li in child.find_all('li'):
                    bullet = li.get_text(strip=True)
                    if bullet:
                        description_parts.append(f"<p>&bull; {bullet}</p>")

            elif child.name == 'div':
                for subchild in child.children:
                    if getattr(subchild, 'name', None) == 'p':
                        text = subchild.get_text(strip=True)
                        if text:
                            description_parts.append(f"<p>{text}</p>")
                    elif subchild.name == 'ul':
                        for li in subchild.find_all('li'):
                            bullet = li.get_text(strip=True)
                            if bullet:
                                description_parts.append(f"<p>&bull; {bullet}</p>")

        formatted_html_description = "\n".join(description_parts)

        ai_prompt = f"{title}\nLocation: {location}\nType: {job_type}\n\n{formatted_html_description}"

        return title, location, job_type, formatted_html_description, ai_prompt

    except requests.RequestException as e:
        print(f"❌ HTTP request failed for job page: {e}")
        return None
    except Exception as e:
        print(f"⚠️ Unexpected error while parsing job content: {e}")
        return None
