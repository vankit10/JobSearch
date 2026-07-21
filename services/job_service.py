from database import create_database, save_jobs
from notifier.email import EmailNotifier
from scrapers.greenhouse import GreenhouseScraper
from utils.exporter import CSVExporter
from utils.filters import is_ios_job, is_location_match
from utils.logger import logger


class JobService:

    def __init__(self):

        # Add more scrapers here in future
        self.scrapers = [
            GreenhouseScraper(),
        ]

    def fetch_jobs(self):

        logger.info("Starting job download...")

        all_jobs = []

        for scraper in self.scrapers:

            try:

                jobs = scraper.fetch_jobs()

                logger.info(
                    f"{scraper.__class__.__name__}: {len(jobs)} jobs downloaded"
                )

                all_jobs.extend(jobs)

            except Exception as e:

                logger.error(
                    f"{scraper.__class__.__name__}: {e}"
                )

        return all_jobs

    def filter_jobs(self, jobs):

        logger.info("Filtering iOS jobs...")

        filtered = [

            job

            for job in jobs

            if is_ios_job(job)
            and is_location_match(job)

        ]

        logger.info(f"{len(filtered)} jobs matched filters")

        return filtered

    def save_jobs(self, jobs):

        logger.info("Saving jobs into database...")

        new_jobs = save_jobs(jobs)

        logger.info(f"{len(new_jobs)} new jobs saved")

        return new_jobs

    def export_jobs(self, jobs):

        if not jobs:

            logger.info("No jobs to export")

            return None

        csv_file = CSVExporter.export(jobs)

        logger.info(f"CSV exported : {csv_file}")

        return csv_file

    def notify(self, jobs):

        if not jobs:

            logger.info("No email notification required")

            print("📭 No new jobs to notify.")

            return

        EmailNotifier().send(jobs)

        logger.info("Email notification sent")

    def print_jobs(self, jobs):

        if not jobs:

            print("\nℹ️ No new jobs found.")

            print("All matching jobs already exist in the database.\n")

            return

        print("\n" + "=" * 70)
        print("📋 New Job Listings")
        print("=" * 70)

        for index, job in enumerate(jobs, start=1):

            print(f"\nJob #{index}")

            print(job)

    def print_summary(
        self,
        downloaded,
        filtered,
        saved
    ):

        print("\n" + "=" * 70)
        print("📊 SUMMARY")
        print("=" * 70)

        print(f"Downloaded Jobs : {downloaded}")
        print(f"Filtered Jobs   : {filtered}")
        print(f"New Jobs Saved  : {saved}")

    def run(self):

        logger.info("=" * 60)
        logger.info("Job Agent Started")

        print("\n" + "=" * 70)
        print("🚀 Job Agent Started")
        print("=" * 70)

        # Create database
        create_database()

        # Download jobs
        all_jobs = self.fetch_jobs()

        print(f"\n📥 Total Jobs Downloaded : {len(all_jobs)}")

        # Filter jobs
        ios_jobs = self.filter_jobs(all_jobs)

        print(f"📱 iOS Jobs Found        : {len(ios_jobs)}")

        # Save jobs
        new_jobs = self.save_jobs(ios_jobs)

        print(f"💾 New Jobs Saved       : {len(new_jobs)}")

        # Export CSV
        csv_file = self.export_jobs(new_jobs)

        if csv_file:

            print(f"📄 CSV Exported         : {csv_file}")

        # Send email
        self.notify(new_jobs)

        # Print jobs
        self.print_jobs(new_jobs)

        # Summary
        self.print_summary(

            downloaded=len(all_jobs),

            filtered=len(ios_jobs),

            saved=len(new_jobs)

        )

        logger.info("Job Agent Finished")

        print("\n" + "=" * 70)
        print("✅ Job Agent Finished")
        print("=" * 70)
        