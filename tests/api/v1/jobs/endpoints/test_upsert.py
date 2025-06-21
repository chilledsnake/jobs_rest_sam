import pytest
from fastapi import status

from app.modules.jobs.repository import JobRepository
from app.modules.jobs.schema import JobSchema


@pytest.mark.parametrize(
    "company, timestamp, data, expected_http_status_code",
    [
        pytest.param(
            "Test Company",
            "2023-04-01T12:00:00Z",
            {"description": "Test"},
            status.HTTP_200_OK,
            id="update",
        ),
        pytest.param(
            "Test Company Insert",
            "Test Company Insert",
            {"description": "Test"},
            status.HTTP_200_OK,
            id="insert",
        ),
    ],
)
async def test_upsert_job(
    mock_dynamodb,
    client,
    company,
    timestamp,
    data,
    expected_http_status_code,
):
    job_repository = JobRepository()
    job_repository.jobs_table.put_item(
        Item={"company": "Test Company", "time_stamp": "2023-04-01T12:00:00Z"}
    )

    response = client.patch(
        f"/v1/jobs/{company}/{timestamp}/",
        json=data,
    )
    assert response.status_code == expected_http_status_code
    assert await job_repository.get_job(company, timestamp) == JobSchema(
        **data, company=company, time_stamp=timestamp
    )
