import schedule
import time

from services.job_service import JobService


class SchedulerService:

    def start(self):

        print("⏰ Scheduler Started")

        # Run immediately once
        JobService().run()

        # Run every hour
        schedule.every(1).hours.do(JobService().run)

        while True:
            schedule.run_pending()
            time.sleep(30)