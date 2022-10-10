from pydantic import BaseModel, Field
from typing import Optional
from .config import examples_of_extra_schema


class Location(BaseModel):
    """
    data structure to save information about classmate location
    """

    country: Optional[str] = Field(default=None, max_length=15, description="Country where classmate live")
    city: Optional[str] = Field(default=None, max_length=25, description="City where classmate is currently living")
    street: Optional[str] = Field(default=None, max_length=25, description="Street where classmate is currently living")
    apartment: Optional[str] = Field(default=None, max_length=5, description="Number of apartment of classmate")


class Classmate(BaseModel):
    """
    Inherits from BaseModel class from Pydantic
    Used to add/create new user in POST request
    """
    name: str = Field(max_length=15, title="Name of the classmate")
    last_name: Optional[str] = Field(default=None, max_length=15, title="Last name of the classmate")
    age: int = Field(gt=0, lt=90, title="Age of the classmate")
    major: Optional[str] = Field(default=None, max_length=40, description="Major of study of current classmate")
    location: Optional[Location] = Field(default=..., description="current location of classmate")

    class Config:
        """
        Class to show FastAPI the examples of valid and invalid input data
        """
        schema_extra = {
            "examples": examples_of_extra_schema
        }


class Classmate_Update(BaseModel):
    """
    Inherits from BaseModel class from Pydantic
    Used as type of value to change existing user in UPDATE request, that is why all the fields are optional
    """
    name: Optional[str] = Field(max_length=15, title="Name of the classmate")
    last_name: Optional[str] = Field(max_length=15, title="Last name of the classmate")
    age: Optional[int] = Field(gt=0, lt=90, title="Age of the classmate")
    major: Optional[str] = Field(default=None, max_length=40, description="Major of study of current classmate")
    location: Optional[Location] = Field(default=None, description="current location of classmate")

    class Config:
        schema_extra = {
            "example":
                {
                    "last_name": "Lisnytskyi",
                    "major": "Computer Science",
                    "location": {
                        "country": "Canada"
                    }
                }
        }
