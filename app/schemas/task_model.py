from pydantic import BaseModel, Field


class Task(BaseModel):
    id:int | None = None 
    title: str = Field(min_length=1, max_length=100)
    description: str | None =Field(default=None, max_length=500)
    status: str = Field(default="pending",)