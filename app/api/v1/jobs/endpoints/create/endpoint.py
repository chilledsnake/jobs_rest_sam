from fastapi import APIRouter, Depends, status

from app.modules.jobs.dependencies import get_job_repository
from app.modules.jobs.repository import JobRepository
from app.modules.jobs.schema import JobSchema

router = APIRouter()


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    description="Create a new job",
    responses={
        503: {"description": "Service Unavailable"},
    },
)
async def create_job(
    data: JobSchema, repo: JobRepository = Depends(get_job_repository)
) -> None:
    """Endpoint to create a new job"""
    await repo.create_job(data=data)
