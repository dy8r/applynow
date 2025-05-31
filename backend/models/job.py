from pydantic import BaseModel
from typing import Optional, List, Literal
from datetime import datetime

class Job(BaseModel):
    id: str
    company: str
    title: str
    location: Optional[str]
    job_type: Optional[str]
    description_html: Optional[str]
    link: str
    salary_min: Optional[int]
    salary_max: Optional[int]
    work_model: Optional[Literal["remote", "on-site", "hybrid"]]
    industry: Optional[str]
    seniority: Optional[Literal["entry", "mid", "senior", "lead"]]
    technologies: List[str]
    is_winnipeg: int
    department: Optional[str]
    min_experience: Optional[int]
    archived: int
    last_seen: Optional[datetime]
    date_added: Optional[datetime]
