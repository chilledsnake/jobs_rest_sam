import logging
import os
from typing import Any, List, Optional

import aioboto3
from botocore.exceptions import ClientError

from app.modules.jobs.schema import JobBaseSchema, JobSchema
from app.utils import ExternalServiceError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

_session = aioboto3.Session()


class JobRepository:
    JOBS_DATA_TABLE_NAME = os.getenv("JOBS_TABLE_NAME", "jobs-table")
    PARTITION_KEY = "company"
    SORT_KEY = "time_stamp"

    _instance: Optional["JobRepository"] = None

    def __init__(self, jobs_table: Any) -> None:
        self.jobs_table = jobs_table

    @classmethod
    async def create(cls) -> "JobRepository":
        """Create or return the singleton JobRepository instance."""
        if cls._instance is None:
            ctx = _session.resource("dynamodb", region_name="eu-central-1")
            dynamodb = await ctx.__aenter__()
            table = await dynamodb.Table(cls.JOBS_DATA_TABLE_NAME)
            cls._instance = cls(jobs_table=table)
        return cls._instance

    async def create_job(self, data: JobSchema) -> None:
        """Create a new job in the DynamoDB table."""
        try:
            await self.jobs_table.put_item(Item=data.model_dump())
        except ClientError as e:
            logger.error(f"Failed to create job: {e}")
            raise ExternalServiceError()

    async def get_job(self, company: str, time_stamp: str) -> JobSchema | None:
        """Retrieve a job from the DynamoDB table by primary key (company and time_stamp)."""
        try:
            response = await self.jobs_table.get_item(
                Key={self.PARTITION_KEY: company, self.SORT_KEY: time_stamp}
            )
        except ClientError as e:
            logger.error(f"Failed to get job: {e}")
            raise ExternalServiceError()

        item = response.get("Item")
        if item:
            return JobSchema(**item)

        return None

    async def list_jobs(self) -> List[Optional[JobBaseSchema]]:
        """List all jobs in the DynamoDB table."""
        try:
            response = await self.jobs_table.scan(
                ProjectionExpression=f"{self.PARTITION_KEY}, {self.SORT_KEY}"
            )
        except ClientError as e:
            logger.error(f"Failed to list jobs: {e}")
            raise ExternalServiceError()

        items = response.get("Items", [])
        return [JobBaseSchema(**item) for item in items]

    async def upsert_job(self, data: JobSchema) -> None:
        """Update an existing job in the DynamoDB table."""
        data_dict = data.model_dump(exclude_unset=True)
        key = {
            self.PARTITION_KEY: data_dict.pop("company"),
            self.SORT_KEY: data_dict.pop("time_stamp"),
        }

        update_expression = ", ".join([f"{key} = :{key}" for key in data_dict.keys()])
        expression_attribute_values = {
            f":{key}": value for key, value in data_dict.items()
        }

        try:
            await self.jobs_table.update_item(
                Key=key,
                UpdateExpression=f"SET {update_expression}",
                ExpressionAttributeValues=expression_attribute_values,
            )
        except ClientError as e:
            logger.error(f"Failed to update job: {e}")
            raise ExternalServiceError()

    async def delete_job(self, company: str, time_stamp: str) -> None:
        """Delete a job from the DynamoDB table by primary key (company and time_stamp)."""
        try:
            await self.jobs_table.delete_item(
                Key={self.PARTITION_KEY: company, self.SORT_KEY: time_stamp}
            )
        except ClientError as e:
            logger.error(f"Failed to delete job: {e}")
            raise ExternalServiceError()
