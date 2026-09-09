from pydantic import BaseModel

class Event(BaseModel):
    date: str
    title: str
    location: str
    city: str
    hour: str
    type_event: str
    author: str
    