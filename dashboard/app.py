from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from dashboard.database import (
    get_jobs,
    total_jobs,
    get_sources,
    total_companies,
    total_countries,
    total_sources,
)

import csv
import io

app = FastAPI()

templates = Jinja2Templates(directory="dashboard/templates")

app.mount(
    "/static",
    StaticFiles(directory="dashboard/static"),
    name="static"
)


@app.get("/")
def home(
    request: Request,
    keyword: str = "",
    country: str = "",
    source: str = "",
    sort: str = "company",
    page: int = 1
):

    jobs = get_jobs(
        keyword,
        country,
        source,
        sort,
        page
    )

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "jobs": jobs,
            "keyword": keyword,
            "country": country,
            "source": source,
            "sort": sort,
            "page": page,
            "sources": get_sources(),
            "total_jobs": total_jobs(),
            "total_companies": total_companies(),
            "total_countries": total_countries(),
            "total_sources": total_sources(),
        }
    )


@app.get("/export")
def export_jobs():

    jobs = get_jobs(
        keyword="",
        country="",
        source="",
        sort="company",
        page=1,
        per_page=100000
    )

    output = io.StringIO()

    writer = csv.writer(output)

    writer.writerow([
        "Company",
        "Title",
        "Location",
        "Source",
        "URL"
    ])

    for job in jobs:

        writer.writerow([
            job["company"],
            job["title"],
            job["location"],
            job["source"],
            job["url"]
        ])

    output.seek(0)

    headers = {
        "Content-Disposition":
        "attachment; filename=jobs.csv"
    }

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers=headers
    )