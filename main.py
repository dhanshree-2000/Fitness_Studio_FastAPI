from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from pytz import timezone
import logging

from models import FitnessClass, BookingRequest, Booking
from database import SessionLocal, FitnessClassDB, BookingDB

app = FastAPI(title="Fitness Studio Booking API")

# Logging
logging.basicConfig(level=logging.INFO)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Helper: Convert to IST or any timezone
def convert_timezone(dt, to_tz):
    return dt.astimezone(timezone(to_tz))

@app.get("/classes", response_model=List[FitnessClass])
def get_classes(tz: str = Query("Asia/Kolkata"), db: Session = Depends(get_db)):
    classes = db.query(FitnessClassDB).filter(FitnessClassDB.datetime >= datetime.now()).all()
    return [
        FitnessClass(
            id=c.id,
            name=c.name,
            datetime=convert_timezone(c.datetime.replace(tzinfo=timezone("Asia/Kolkata")), tz),
            instructor=c.instructor,
            available_slots=c.available_slots
        ) for c in classes
    ]

@app.post("/book", response_model=Booking)
def book_class(request: BookingRequest, db: Session = Depends(get_db)):
    fitness_class = db.query(FitnessClassDB).filter(FitnessClassDB.id == request.class_id).first()
    if not fitness_class:
        raise HTTPException(status_code=404, detail="Class not found")
    if fitness_class.available_slots <= 0:
        raise HTTPException(status_code=400, detail="No slots available")
    # Reduce slot
    fitness_class.available_slots -= 1
    booking = BookingDB(
        class_id=request.class_id,
        client_name=request.client_name,
        client_email=request.client_email,
        booked_at=datetime.now()
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    db.commit()
    return Booking(
        id=booking.id,
        class_id=booking.class_id,
        client_name=booking.client_name,
        client_email=booking.client_email,
        booked_at=booking.booked_at
    )

@app.get("/bookings", response_model=List[Booking])
def get_bookings(email: str, db: Session = Depends(get_db)):
    bookings = db.query(BookingDB).filter(BookingDB.client_email == email).all()
    return [
        Booking(
            id=b.id,
            class_id=b.class_id,
            client_name=b.client_name,
            client_email=b.client_email,
            booked_at=b.booked_at
        ) for b in bookings
    ]
