import csv
import os
from datetime import datetime


class CSVExporter:

    @staticmethod
    def export(jobs):

        os.makedirs("reports", exist_ok=True)

        filename = datetime.now().strftime(
            "reports/jobs_%Y_%m_%d_%H_%M.csv"
        )

        with open(filename, "w", newline="", encoding="utf-8") as file:

            writer = csv.writer(file)

            writer.writerow([
                "Company",
                "Title",
                "Location",
                "Source",
                "Link"
            ])

            for job in jobs:

                writer.writerow([
                    job.company,
                    job.title,
                    job.location,
                    job.source,
                    job.url
                ])

        return filename