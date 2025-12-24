# schemas/Flight1.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class Flight(BaseModel):
    flight_id: str
    airline: str
    flight_number: str
    origin: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    price: float
    available_seats: int

class Bookings(BaseModel):
    booking_id: str
    flight_id: str
    passenger_name: str
    num_seats: int
    booking_time: datetime
    status: str

class Search_flights(BaseModel):
    origin: str
    destination: str
    departure_date: str
    passenger: int = 1

class BookingFlight(BaseModel):
    flight_id: str
    passenger_name: str
    num_seats: int