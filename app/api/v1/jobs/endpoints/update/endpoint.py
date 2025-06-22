from fastapi import APIRouter, status

from app.api.v1.jobs.endpoints.update.schema import UpdateJobSchema
from app.modules.jobs.repository import JobRepository
from app.modules.jobs.schema import JobSchema
from app.utils import NotFoundError

router = APIRouter()


@router.patch(
    path="/{company}/{time_stamp}/",
    status_code=status.HTTP_200_OK,
    responses={
        503: {"description": "Service Unavailable"},
    },
    description="Update or insert a job record. If the record does not exist, it will be inserted.",
)
async def upsert_job(company: str, time_stamp: str, data: UpdateJobSchema) -> None:
    await JobRepository().upsert_job(
        JobSchema(
            **data.model_dump(exclude_unset=True),
            company=company,
            time_stamp=time_stamp,
        )
    )
