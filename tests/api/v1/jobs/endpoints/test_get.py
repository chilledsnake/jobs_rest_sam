import pytest
from fastapi import status

from app.modules.jobs.repository import JobRepository
from app.modules.jobs.schema import JobSchema


@pytest.mark.parametrize(
    "company, timestamp, expected_http_status_code, expected_output",
    [
        pytest.param(
            "Test Company",
            "2023-04-01T12:00:00Z",
            status.HTTP_200_OK,
            JobSchema(
                company="Test Company",
                time_stamp="2023-04-01T12:00:00Z",
            ).model_dump(),
            id="valid_input",
        ),
        pytest.param(
            "Test Not Found",
            "Test Not Found",
            status.HTTP_404_NOT_FOUND,
            {"detail": "Resource not found"},
            id="resource_not_found",
        ),
    ],
)
def test_get_job(
    mock_dynamodb,
    client,
    company,
    timestamp,
    expected_http_status_code,
    expected_output,
):
    job_repository = JobRepository()
    job_repository.jobs_table.put_item(
        Item={"company": "Test Company", "time_stamp": "2023-04-01T12:00:00Z"}
    )

    response = client.get(
        f"/v1/jobs/{company}/{timestamp}",
    )
    assert response.status_code == expected_http_status_code
    assert response.json() == expected_output
