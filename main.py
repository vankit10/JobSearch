from database import create_database
from scrapers.greenhouse import GreenhouseScraper


def main():

    create_database()

    scraper = GreenhouseScraper()

    jobs = scraper.fetch_jobs()

    print(f"\nFound {len(jobs)} jobs\n")

    for job in jobs:
        print(job)


if __name__ == "__main__":
    main()