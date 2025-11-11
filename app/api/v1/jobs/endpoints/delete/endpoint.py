from fastapi import APIRouter, status

from app.modules.jobs.repository import JobRepository

router = APIRouter()


@router.delete(
    path="/{company}/{time_stamp}/",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete job",
    responses={
        503: {"description": "Service Unavailable"},
    },
)
async def delete_job(company: str, time_stamp: str) -> None:
    """Endpoint to create a new job"""
    await JobRepository().delete_job(company=company, time_stamp=time_stamp)
