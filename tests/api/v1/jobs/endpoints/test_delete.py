import pytest
from fastapi import status

from app.modules.jobs.repository import JobRepository


@pytest.mark.parametrize(
    "company, timestamp, expected_http_status_code",
    [
        pytest.param(
            "Test Company",
            "2023-04-01T12:00:00Z",
            status.HTTP_204_NO_CONTENT,
            id="delete_existing_job",
        ),
        pytest.param(
            "Test Non Existent Company",
            "Test Non Existent Company",
            status.HTTP_204_NO_CONTENT,
            id="delete_nonexistent_job",
        ),
    ],
)
async def test_get_job(
    mock_dynamodb,
    client,
    company,
    timestamp,
    expected_http_status_code,
):
    job_repository = JobRepository()
    job_repository.jobs_table.put_item(
        Item={"company": "Test Company", "time_stamp": "2023-04-01T12:00:00Z"}
    )

    response = client.delete(
        f"/v1/jobs/{company}/{timestamp}",
    )
    assert response.status_code == expected_http_status_code
    response = await job_repository.get_job(company, timestamp)
    assert response is None
