import pytest
from fastapi import status

from app.modules.jobs.repository import JobRepository
from app.modules.jobs.schema import JobBaseSchema


@pytest.mark.parametrize(
    "input_data, expected_http_status_code",
    [
        pytest.param(
            [
                {"company": "Test Company", "time_stamp": "2023-04-01T12:00:00Z"},
                {"company": "Another Company", "time_stamp": "2023-04-02T12:00:00Z"},
            ],
            status.HTTP_200_OK,
            id="valid_input",
        ),
        pytest.param(
            [],
            status.HTTP_200_OK,
            id="no_data",
        ),
    ],
)
def test_list_jobs(mock_dynamodb, client, input_data, expected_http_status_code):
    # Insert test data into the database
    for item in input_data:
        JobRepository().jobs_table.put_item(Item=item)

    response = client.get(
        "/v1/jobs/",
    )
    assert response.status_code == expected_http_status_code
    assert isinstance(response.json(), list)
    for job in input_data:
        assert JobBaseSchema(**job).model_dump() in response.json()
