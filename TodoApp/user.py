from typing import Optional
from pydantic import BaseModel, Field

class CreateUser(BaseModel):
    username: str = Field(min_length=3)
    email: Optional[str]
    first_name: str = Field(min_length=3)
    last_name: str = Field(min_length=3)
    password: str

