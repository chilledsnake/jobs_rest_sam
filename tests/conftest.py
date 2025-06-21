import boto3
import pytest
from fastapi.testclient import TestClient
from moto import mock_aws

from app.main import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
def mock_dynamodb(request):
    with mock_aws():
        dynamodb = boto3.resource("dynamodb", region_name="eu-central-1")

        dynamodb.create_table(
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
