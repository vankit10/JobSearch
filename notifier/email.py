import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import EMAIL
from config import EMAIL_PASSWORD
from config import RECEIVER_EMAIL


class EmailNotifier:

    def send(self, jobs):

        if not jobs:
            print("📭 No new jobs to email.")
            return

        subject = f"🚀 {len(jobs)} New iOS Jobs Found"

        body = ""

        for job in jobs:

            body += f"""
Company : {job.company}

Title : {job.title}

Location : {job.location}

Source : {job.source}

Apply : {job.url}

------------------------------------------------------------

"""

        message = MIMEMultipart()

        message["From"] = EMAIL
        message["To"] = RECEIVER_EMAIL
        message["Subject"] = subject

        message.attach(MIMEText(body, "plain"))

        try:

            server = smtplib.SMTP("smtp.gmail.com", 587)

            server.starttls()

            server.login(
                EMAIL,
                EMAIL_PASSWORD
            )

            server.sendmail(
                EMAIL,
                RECEIVER_EMAIL,
                message.as_string()
            )

            server.quit()

            print("✅ Email sent successfully!")

        except Exception as e:

            print("❌ Email failed")

            print(e)