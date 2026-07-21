import json
import requests

from utils.job import Job


class LeverScraper:

    def fetch_jobs(self):

        with open("data/lever_companies.json", "r") as file:
            companies = json.load(file)

        all_jobs = []

        print(f"\nLoaded {len(companies)} Lever companies\n")

        for company in companies:

            board = company["board"]

            url = f"https://api.lever.co/v0/postings/{board}?mode=json"

            print("=" * 60)
            print(f"Searching: {company['name']}")
            print(f"Board    : {board}")

            try:

                response = requests.get(url, timeout=15)

                if response.status_code == 404:
                    print("❌ Board not found")
                    continue

                if response.status_code != 200:
                    print(f"❌ HTTP {response.status_code}")
                    continue

                jobs = response.json()

                print(f"✅ Found {len(jobs)} jobs")

                for job in jobs:

                    location = ""

                    if job.get("categories"):
                        location = job["categories"].get("location", "")

                    all_jobs.append(

                        Job(
                            title=job.get("text", ""),
                            company=company["name"],
                            location=location,
                            url=job.get("hostedUrl", ""),
                            source="Lever"
                        )

                    )

            except Exception as e:
                print(e)

        print(f"\nTotal Lever Jobs : {len(all_jobs)}")

        return all_jobs