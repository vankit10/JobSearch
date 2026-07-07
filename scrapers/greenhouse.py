from scrapers.base import BaseScraper
from utils.job import Job


class GreenhouseScraper(BaseScraper):

    def fetch_jobs(self):

        jobs = [

            Job(
                title="iOS Developer",
                company="Apple",
                location="Germany",
                url="https://apple.com",
                source="Greenhouse"
            ),

            Job(
                title="Swift Developer",
                company="BMW",
                location="Munich",
                url="https://bmw.com",
                source="Greenhouse"
            )

        ]

        return jobs