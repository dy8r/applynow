import time
from parser import payworks, skipthedishes, neo, priceline, bold, pollard
import random

def main():
    while True:
        payworks.extract_job_postings()
        neo.extract_job_postings()
        priceline.extract_job_postings()
        bold.extract_job_postings()
        pollard.extract_job_postings()
        tts = random.randint(60, 300)
        print(f"Sleeping for {tts} seconds before next cycle...")
        time.sleep(tts)