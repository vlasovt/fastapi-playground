from typing import Optional
from pydantic import BaseModel, Field

class Todo(BaseModel):
    id: Optional[int]
    title: str = Field(min_length=3)
    description: Optional[str] = Field(min_length=3)
    priority: int = Field(gt=0, lt=6, description="The priority must be between 1 and 5")
    complete: bool = Field(default=False)
    class Config:
        schema_extra = {
            "example": {
                "title": "Get something done",
                "description": "A very nice description of a priority",
                "priority": 5,
                "complete": False,
            }
        }

