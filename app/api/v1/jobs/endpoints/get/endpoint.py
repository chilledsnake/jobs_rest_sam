from fastapi import APIRouter, status

from app.modules.jobs.repository import JobRepository
from app.modules.jobs.schema import JobSchema
from app.utils import NotFoundError

router = APIRouter()


@router.get(
    path="/{company}/{time_stamp}/",
    status_code=status.HTTP_200_OK,
    response_model=JobSchema,
    responses={
        200: {"description": "Successful response"},
        404: {"description": "Resource not found"},
        503: {"description": "Service Unavailable"},
    },
    description="Retrieve a job by company and timestamp",
)
async def get_job(company: str, time_stamp: str) -> JobSchema:
    if job := await JobRepository().get_job(company=company, time_stamp=time_stamp):
        return job
    raise NotFoundError()
