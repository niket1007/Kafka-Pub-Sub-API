from pydantic import BaseModel, Field
from typing import Literal

class RequestPayload(BaseModel):
    id: str = Field(description="Student Roll Number")
    name: str = Field(description="Student Full Name")
    classs: int = Field(description="Student Class")
    class_teacher: str = Field(description="Student Class Teacher Name")

class ResponsePayload(BaseModel):
    status: Literal["Success", "Failure"] = Field(description="Publish status")
    message: str = Field(description="Publish status message")
