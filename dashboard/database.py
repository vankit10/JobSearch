import sqlite3
import os

DB_NAME = os.path.abspath("jobs.db")

print(f"Using database:\n{DB_NAME}")


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def get_jobs(
        keyword="",
        country="",
        source="",
        sort="company",
        page=1,
        per_page=20
):

    conn = get_connection()

    cursor = conn.cursor()

    query = """
        SELECT *
        FROM jobs
        WHERE 1=1
    """

    params = []

    if keyword:

        query += """
        AND
        (
            company LIKE ?
            OR title LIKE ?
        )
        """

        params.append(f"%{keyword}%")
        params.append(f"%{keyword}%")

    if country:

        query += " AND location LIKE ?"

        params.append(f"%{country}%")

    if source:

        query += " AND source = ?"

        params.append(source)

    allowed = [
        "company",
        "title",
        "location",
        "source"
    ]

    if sort not in allowed:
        sort = "company"

    query += f" ORDER BY {sort}"

    offset = (page - 1) * per_page

    query += " LIMIT ? OFFSET ?"

    params.append(per_page)
    params.append(offset)

    cursor.execute(query, params)

    jobs = cursor.fetchall()

    conn.close()

    return jobs


def get_job(job_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM jobs
        WHERE id = ?
        """,
        (job_id,)
    )

    job = cursor.fetchone()

    conn.close()

    return job


def total_jobs():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM jobs")

    total = cursor.fetchone()[0]

    conn.close()

    return total


def get_sources():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT DISTINCT source
        FROM jobs
        ORDER BY source
        """
    )

    data = [row[0] for row in cursor.fetchall()]

    conn.close()

    return data


def total_companies():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(DISTINCT company)
        FROM jobs
        """
    )

    total = cursor.fetchone()[0]

    conn.close()

    return total


def total_countries():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(DISTINCT location)
        FROM jobs
        """
    )

    total = cursor.fetchone()[0]

    conn.close()

    return total


def total_sources():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(DISTINCT source)
        FROM jobs
        """
    )

    total = cursor.fetchone()[0]

    conn.close()

    return total