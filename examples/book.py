from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID

class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=3)
    author: str = Field(min_length=3, max_length=100)
    description: Optional[str] = Field(min_length=3)
    rating: int = Field(gt=-1, lt=101)
    class Config:
        schema_extra = {
            "example": {
                "id": "11f4c2ea-1340-41f4-89f7-2852347bb0d1",
                "title": "Computer Science Pro",
                "author": "Codingwithroby",
                "description": "A very nice description of a book",
                "rating": 75
            }
        }

class BookNoRating(BaseModel):
    id: UUID
    title: str = Field(min_length=3)
    author: str = Field(min_length=3, max_length=100)
    description: Optional[str] = Field(min_length=3)

