import aioboto3
import pytest
from fastapi.testclient import TestClient
from aiomoto import mock_aws as mock_aws_async

from app.main import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
async def mock_dynamodb(request):
    from app.modules.jobs import repository

    # Reset singleton so each test gets a fresh repository
    repository.JobRepository._instance = None

    with mock_aws_async():
        async with aioboto3.Session().resource(
            "dynamodb", region_name="eu-central-1"
        ) as dynamodb:
            await dynamodb.create_table(
                TableName="jobs-table",
                KeySchema=[
                    {"AttributeName": "company", "KeyType": "HASH"},
                    {"AttributeName": "time_stamp", "KeyType": "RANGE"},
                ],
                AttributeDefinitions=[
                    {"AttributeName": "company", "AttributeType": "S"},
                    {"AttributeName": "time_stamp", "AttributeType": "S"},
                ],
                ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
            )
            yield
