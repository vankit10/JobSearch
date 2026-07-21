from config import KEYWORDS, COUNTRIES


def is_ios_job(job):
    """
    Returns True if the job title looks like an iOS job.
    """
    title = job.title.lower()

    return any(keyword in title for keyword in KEYWORDS)


def is_location_match(job):
    """
    Returns True if the job location matches one of the preferred countries.
    """
    location = job.location.lower()

    return any(country in location for country in COUNTRIES)