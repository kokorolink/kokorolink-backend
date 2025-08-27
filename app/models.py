from typing import Optional, List
from datetime import datetime
from uuid import uuid4
from sqlmodel import SQLModel, Field, Relationship

def cuid() -> str:
    # simple unique id; replace with real CUID/UUID later if you like
    return str(uuid4())

class Event(SQLModel, table=True):
    id: str = Field(default_factory=cuid, primary_key=True)
    title: str
    slug: str = Field(index=True, unique=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    guests: List["Guest"] = Relationship(back_populates="event")

class Guest(SQLModel, table=True):
    id: str = Field(default_factory=cuid, primary_key=True)
    email: str = Field(index=True, unique=True)
    name: Optional[str] = None
    rsvp: Optional[str] = Field(default=None)  # YES | NO | MAYBE
    created_at: datetime = Field(default_factory=datetime.utcnow)
    event_id: Optional[str] = Field(default=None, foreign_key="event.id")
    event: Optional[Event] = Relationship(back_populates="guests")
