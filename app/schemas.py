from typing import Optional
from pydantic import BaseModel

class EventCreate(BaseModel):
  title: str
  slug: str

class GuestCreate(BaseModel):
  email: str
  name: Optional[str] = None
  rsvp: Optional[str] = None
