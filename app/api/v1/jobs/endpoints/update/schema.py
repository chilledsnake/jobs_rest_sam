from typing import Optional

from pydantic import BaseModel, Field


class UpdateJobSchema(BaseModel):
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
