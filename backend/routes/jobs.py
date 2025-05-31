from fastapi import APIRouter, Request, Query, Path, HTTPException
from utils.limiter import limiter
from models.job import Job
from pydantic import BaseModel
from database.queries import get_jobs, get_job_by_id
from typing import List, Optional
from database.utils import sanitize_filters

router = APIRouter(prefix="/jobs", tags=["Jobs"])

class JobListResponse(BaseModel):
    data: List[Job]
    total: int
    page: int
    page_size: int

@router.get("/", response_model=JobListResponse)
@limiter.limit("30/minute")
def list_jobs(
    request: Request,
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),

    # Filters
    company: Optional[List[str]] = Query(None),
    title: Optional[List[str]] = Query(None),
    location: Optional[List[str]] = Query(None),
    job_type: Optional[List[str]] = Query(None),
    department: Optional[List[str]] = Query(None),
    industry: Optional[List[str]] = Query(None),
    work_model: Optional[List[str]] = Query(None),
    seniority: Optional[List[str]] = Query(None),
    technologies: Optional[List[str]] = Query(None),

    is_winnipeg: Optional[bool] = Query(None),
    is_swe: Optional[bool] = Query(None),

    salary_min: Optional[float] = Query(None),
    salary_max: Optional[float] = Query(None),
    min_experience: Optional[float] = Query(None),
):
    
    filters = sanitize_filters({
        "company": company,
        "title": title,
        "location": location,
        "job_type": job_type,
        "department": department,
        "industry": industry,
        "work_model": work_model,
        "seniority": seniority,
        "technologies": technologies,
        "is_winnipeg": is_winnipeg,
        "salary_min": salary_min,
        "salary_max": salary_max,
        "min_experience": min_experience,
        "is_swe": is_swe
    },
        strict_sql=True
    )
    return get_jobs(
        offset=offset,
        limit=limit,
        **filters
    )


@router.get("/{job_id}", response_model=Job)
@limiter.limit("60/minute")
def get_job(request: Request, job_id: str = Path(..., description="ID of the job to fetch")):
    job = get_job_by_id(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job