import pytest
from fastapi import status


@pytest.mark.parametrize(
    "input_data, expected_http_status_code, expected_output",
    [
        pytest.param(
            {
                "company": "Test Company",
                "time_stamp": "2023-04-01T12:00:00Z",
                "title": "Test Title",
            },
            status.HTTP_201_CREATED,
            None,
            id="valid_input",
        ),
        pytest.param(
            {
                "company": "",
                "time_stamp": "2023-04-01T12:00:00Z",
                "title": "Test Title",
            },
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            {
                "detail": [
                    {
                        "type": "string_too_short",
                        "loc": ["body", "company"],
                        "msg": "String should have at least 1 character",
                        "input": "",
                        "ctx": {"min_length": 1},
                    }
                ]
            },
            id="empty_company",
        ),
        pytest.param(
            {"company": "Test Company", "time_stamp": "", "title": "Test Title"},
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            {
                "detail": [
                    {
                        "type": "string_too_short",
                        "loc": ["body", "time_stamp"],
                        "msg": "String should have at least 1 character",
                        "input": "",
                        "ctx": {"min_length": 1},
                    }
                ]
            },
            id="empty_timestamp",
        ),
    ],
)
def test_create_job(
    mock_dynamodb, client, input_data, expected_http_status_code, expected_output
):
    response = client.post(
        "/v1/jobs/",
        json=input_data,
    )
    assert response.status_code == expected_http_status_code
    assert response.json() == expected_output
