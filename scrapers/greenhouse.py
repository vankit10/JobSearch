import json
import requests

from utils.job import Job


class GreenhouseScraper:

    def fetch_jobs(self):

        # Load company list
        with open("data/greenhouse_companies.json", "r") as file:
            companies = json.load(file)

        all_jobs = []

        print(f"\nLoaded {len(companies)} Greenhouse companies\n")

        for company in companies:

            board = company["board"]

            url = f"https://boards-api.greenhouse.io/v1/boards/{board}/jobs"

            print("=" * 60)
            print(f"Searching: {company['name']}")
            print(f"Board    : {board}")

            try:

                response = requests.get(url, timeout=15)

                if response.status_code == 404:
                    print("❌ Board not found")
                    continue

                elif response.status_code == 403:
                    print("❌ Access Forbidden")
                    continue

                elif response.status_code != 200:
                    print(f"❌ HTTP Error : {response.status_code}")
                    continue

                data = response.json()

                jobs = data.get("jobs", [])

                print(f"✅ Found {len(jobs)} jobs")

                for job in jobs:

                    title = job.get("title", "N/A")

                    location = ""

                    if job.get("location"):
                        location = job["location"].get("name", "")

                    absolute_url = job.get("absolute_url", "")

                    all_jobs.append(

                        Job(
                            title=title,
                            company=company["name"],
                            location=location,
                            url=absolute_url,
                            source="Greenhouse"
                        )

                    )

            except requests.exceptions.Timeout:
                print("⏰ Request Timed Out")

            except requests.exceptions.ConnectionError:
                print("🌐 Connection Error")

            except requests.exceptions.RequestException as e:
                print(f"❌ Request Error : {e}")

            except Exception as e:
                print(f"❌ Unexpected Error : {e}")

        print("\n" + "=" * 60)
        print(f"Total Jobs Downloaded : {len(all_jobs)}")
        print("=" * 60)

        return all_jobs