from unittest.mock import patch

import pytest
from botocore.exceptions import ClientError

from app.modules.jobs.repository import JobRepository
from app.modules.jobs.schema import JobBaseSchema, JobSchema
from app.utils import ExternalServiceError


async def test_create_and_get_job(mock_dynamodb):
    job_repository = JobRepository()
    job_data = {
        "company": "TestCompany",
        "time_stamp": "2023-10-01T12:00:00Z",
        "description": "Sample Job",
    }
    job_base_schema = JobSchema(**job_data)
    await job_repository.create_job(job_base_schema)
    response = await job_repository.get_job(
        company="TestCompany", time_stamp="2023-10-01T12:00:00Z"
    )
    assert response == JobSchema(**job_data)


async def test_get_job_not_found(mock_dynamodb):
    assert (
        await JobRepository().get_job(
            company="not_existing_company", time_stamp="not_existing_time_stamp"
        )
        is None
    )


async def test_list_jobs(mock_dynamodb):
    job_repository = JobRepository()
    job_data1 = {
        "company": "TestCompany",
        "time_stamp": "2023-10-01T12:00:00Z",
        "description": "Sample Job 1",
    }
    job_data2 = {
        "company": "AnotherCompany",
        "time_stamp": "2023-10-02T12:00:00Z",
        "description": "Sample Job 2",
    }
    await job_repository.create_job(JobSchema(**job_data1))
    await job_repository.create_job(JobSchema(**job_data2))
    jobs = await job_repository.list_jobs()
    assert len(jobs) == 2
    for job in jobs:
        assert isinstance(job, JobBaseSchema)
        assert job.company in ["TestCompany", "AnotherCompany"]
        assert job.time_stamp in ["2023-10-01T12:00:00Z", "2023-10-02T12:00:00Z"]


async def test_update_and_get_job(mock_dynamodb):
    job_repository = JobRepository()
    job_data = {
        "company": "TestCompany",
        "time_stamp": "2023-10-01T12:00:00Z",
        "description": "Sample Job 1",
    }
    await job_repository.create_job(JobSchema(**job_data))
    updated_description = "Updated Job Description"
    await job_repository.upsert_job(
        JobSchema(
            company="TestCompany",
            time_stamp="2023-10-01T12:00:00Z",
            description=updated_description,
        )
    )
    job = await job_repository.get_job("TestCompany", "2023-10-01T12:00:00Z")
    assert isinstance(job, JobSchema)
    assert job.description == updated_description


async def test_update_not_found_created(mock_dynamodb):
    job_repository = JobRepository()
    await job_repository.upsert_job(
        JobSchema(
            company="TestCompany",
            time_stamp="2023-10-01T12:00:00Z",
            description="Test description",
        )
    )
    job = await job_repository.get_job("TestCompany", "2023-10-01T12:00:00Z")
    assert isinstance(job, JobSchema)
    assert job.description == "Test description"


async def test_delete_job(mock_dynamodb):
    job_repository = JobRepository()
    job_data = {
        "company": "TestCompany",
        "time_stamp": "2023-10-01T12:00:00Z",
        "description": "Sample Job",
    }
    job_base_schema = JobSchema(**job_data)
    await job_repository.create_job(job_base_schema)
    response = await job_repository.get_job(
        company="TestCompany", time_stamp="2023-10-01T12:00:00Z"
    )
    assert response == JobSchema(**job_data)

    await job_repository.delete_job("TestCompany", "2023-10-01T12:00:00Z")
    response = await job_repository.get_job(
        company="TestCompany", time_stamp="2023-10-01T12:00:00Z"
    )
    assert response is None


async def test_delete_not_existing_job(mock_dynamodb):
    job_repository = JobRepository()

    await job_repository.delete_job("TestCompany", "2023-10-01T12:00:00Z")
    response = await job_repository.get_job(
        company="TestCompany", time_stamp="2023-10-01T12:00:00Z"
    )
    assert response is None


async def test_create_job_client_error(mock_dynamodb):
    job_repository = JobRepository()
    job_data = {
        "company": "TestCompany",
        "time_stamp": "2023-10-01T12:00:00Z",
        "description": "Sample Job",
    }
    job_base_schema = JobSchema(**job_data)

    with patch.object(
        job_repository.jobs_table,
        "put_item",
        side_effect=ClientError(
            {"Error": {"Code": "ValidationException", "Message": "Error"}},
            "PutItem",
        ),
    ):
        with pytest.raises(ExternalServiceError):
            await job_repository.create_job(job_base_schema)


async def test_get_job_client_error(mock_dynamodb):
    job_repository = JobRepository()

    with patch.object(
        job_repository.jobs_table,
        "get_item",
        side_effect=ClientError(
            {"Error": {"Code": "ValidationException", "Message": "Error"}},
            "GetItem",
        ),
    ):
        with pytest.raises(ExternalServiceError):
            await job_repository.get_job("TestCompany", "2023-10-01T12:00:00Z")


async def test_list_jobs_client_error(mock_dynamodb):
    job_repository = JobRepository()

    with patch.object(
        job_repository.jobs_table,
        "scan",
        side_effect=ClientError(
            {"Error": {"Code": "ValidationException", "Message": "Error"}},
            "Scan",
        ),
    ):
        with pytest.raises(ExternalServiceError):
            await job_repository.list_jobs()


async def test_upsert_job_client_error(mock_dynamodb):
    job_repository = JobRepository()
    job_data = {
        "company": "TestCompany",
        "time_stamp": "2023-10-01T12:00:00Z",
        "description": "Sample Job",
    }

    with patch.object(
        job_repository.jobs_table,
        "update_item",
        side_effect=ClientError(
            {"Error": {"Code": "ValidationException", "Message": "Error"}},
            "UpdateItem",
        ),
    ):
        with pytest.raises(ExternalServiceError):
            await job_repository.upsert_job(JobSchema(**job_data))


async def test_delete_job_client_error(mock_dynamodb):
    job_repository = JobRepository()

    with patch.object(
        job_repository.jobs_table,
        "delete_item",
        side_effect=ClientError(
            {"Error": {"Code": "ValidationException", "Message": "Error"}},
            "DeleteItem",
        ),
    ):
        with pytest.raises(ExternalServiceError):
            await job_repository.delete_job("TestCompany", "2023-10-01T12:00:00Z")
