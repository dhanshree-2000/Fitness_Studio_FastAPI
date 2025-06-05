from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

class FitnessClass(BaseModel):
    id: int
    name: str
    datetime: datetime
    instructor: str
    available_slots: int

class BookingRequest(BaseModel):
    class_id: int
    client_name: str = Field(..., min_length=1)
    client_email: EmailStr

class Booking(BaseModel):
    id: int
    class_id: int
    client_name: str
    client_email: EmailStr
    booked_at: datetime
