import sqlite3
from config import DATABASE


def create_database():
    """
    Creates the jobs table if it doesn't already exist.
    """

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            location TEXT,
            url TEXT UNIQUE NOT NULL,
            source TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def save_jobs(jobs):
    """
    Saves jobs to the database.

    Returns:
        list -> only newly inserted jobs
    """

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    new_jobs = []

    for job in jobs:

        try:

            cursor.execute("""
                INSERT INTO jobs
                (title, company, location, url, source)
                VALUES (?, ?, ?, ?, ?)
            """, (
                job.title,
                job.company,
                job.location,
                job.url,
                job.source
            ))

            new_jobs.append(job)

        except sqlite3.IntegrityError:
            # Duplicate URL already exists
            pass

    conn.commit()
    conn.close()

    return new_jobs


def get_all_jobs():
    """
    Returns all jobs stored in the database.
    """

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            title,
            company,
            location,
            url,
            source,
            created_at
        FROM jobs
        ORDER BY created_at DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


def total_jobs():
    """
    Returns total number of jobs in database.
    """

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM jobs")

    count = cursor.fetchone()[0]

    conn.close()

    return count


def clear_database():
    """
    Deletes all jobs.
    """

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM jobs")

    conn.commit()
    conn.close()

    print("🗑 Database cleared successfully.")