from pydantic import BaseModel, Field


class Task(BaseModel):
    id:int | None = None 
    title: str = Field(min_length=1, max_length=100)
    completed: bool = Field(default=False)