from typing import List

from fastapi import APIRouter, status

from app.modules.jobs.repository import JobRepository
from app.modules.jobs.schema import JobBaseSchema

router = APIRouter()


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=List[JobBaseSchema],
    responses={
        200: {"description": "Successful response"},
        503: {"description": "Service Unavailable"},
    },
    description="Endpoint to list all jobs",
)
async def list_jobs() -> List[JobBaseSchema | None]:
    return await JobRepository().list_jobs()
