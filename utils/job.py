from dataclasses import dataclass


@dataclass
class Job:
    def __init__(
        self,
        title,
        company,
        location,
        url,
        source,
        description="",
        department="",
        employment_type="",
        salary=""
    ):
        self.title = title
        self.company = company
        self.location = location
        self.url = url
        self.source = source
        self.description = description
        self.department = department
        self.employment_type = employment_type
        self.salary = salary