from pydantic import BaseModel, Field
from .config import examples_of_extra_schema


class Location(BaseModel):
    """
    data structure to save information about classmate location
    """

    country: str | None = Field(default=None, max_length=15, description="Country where classmate live")
    city: str | None = Field(default=None, max_length=25, description="City where classmate is currently living")
    street: str | None = Field(default=None, max_length=25, description="Street where classmate is currently living")
    apartment: str | None = Field(default=None, max_length=5, description="Number of apartment of classmate")


class ClassmateIn(BaseModel):
    """
    Inherits from BaseModel class from Pydantic
    Used to add/create new user in POST request
    """
    name: str = Field(max_length=15, title="Name of the classmate")
    last_name: str | None = Field(default=None, max_length=15, title="Last name of the classmate")
    age: int = Field(gt=0, lt=90, title="Age of the classmate")
    major: str | None = Field(default=None, max_length=40, description="Major of study of current classmate")
    location: Location = Field(default=..., description="current location of classmate")

    class Config:
        """
        Class to show FastAPI the examples of valid and invalid input data
        """
        schema_extra = {
            "examples": examples_of_extra_schema
        }


class ClassmateOut(ClassmateIn):
    """
    Inherits from BaseModel class from Pydantic
    Used to add/create new user in POST request
    """
    classmate_id: int = Field(default=..., title="ID of classmate in database")


class ClassmateUpdate(ClassmateIn):
    """
    Inherits from BaseModel class from Pydantic
    Used as type of value to change existing user in UPDATE request, that is why all the fields are optional
    """
    name: str | None = Field(max_length=15, title="Name of the classmate")
    age: int | None = Field(gt=0, lt=90, title="Age of the classmate")
    location: Location | None = Field(default=None, description="current location of classmate")

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
