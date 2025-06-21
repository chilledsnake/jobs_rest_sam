from typing import Optional

from pydantic import BaseModel, Field


class JobBaseSchema(BaseModel):
    company: str = Field(
        ..., min_length=1, description="The name of the company offering the job."
    )
    time_stamp: str = Field(
        ..., min_length=1, description="The time_stamp when the job was posted."
    )


class JobSchema(JobBaseSchema):
    title: Optional[str] = Field(
        "", description="The title of the job.", examples=["Software Engineer"]
    )
    description: Optional[str] = Field(
        "",
        description="A brief description of the job.",
        examples=["We are looking for a talented software engineer..."],
    )
    salary: Optional[int] = Field(
        None, description="The salary offered for the job.", examples=[100000]
    )
