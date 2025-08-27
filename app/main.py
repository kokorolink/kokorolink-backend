import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import select, Session
from .db import init_db, get_session
from .models import Event, Guest
from .schemas import EventCreate, GuestCreate

app = FastAPI(title="KokoroLink API")

origins = [os.getenv("CORS_ORIGIN", "http://localhost:3000")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/health")
def health():
    return {"ok": True, "service": "backend", "framework": "fastapi"}

@app.post("/events", response_model=dict)
def create_event(payload: EventCreate, session: Session = Depends(get_session)):
    exists = session.exec(select(Event).where(Event.slug == payload.slug)).first()
    if exists:
        raise HTTPException(status_code=409, detail="slug already exists")
    event = Event(title=payload.title, slug=payload.slug)
    session.add(event)
    session.commit()
    session.refresh(event)
    return {"id": event.id, "slug": event.slug, "title": event.title}

@app.get("/events/{slug}", response_model=dict)
def get_event(slug: str, session: Session = Depends(get_session)):
    event = session.exec(select(Event).where(Event.slug == slug)).first()
    if not event:
        raise HTTPException(status_code=404, detail="not found")
    return {"id": event.id, "slug": event.slug, "title": event.title}

@app.post("/events/{slug}/guests", response_model=dict)
def add_guest(slug: str, payload: GuestCreate, session: Session = Depends(get_session)):
    event = session.exec(select(Event).where(Event.slug == slug)).first()
    if not event:
        raise HTTPException(status_code=404, detail="event not found")
    guest = Guest(email=payload.email, name=payload.name, rsvp=payload.rsvp, event_id=event.id)
    session.add(guest)
    session.commit()
    session.refresh(guest)
    return {"id": guest.id, "email": guest.email, "rsvp": guest.rsvp}
