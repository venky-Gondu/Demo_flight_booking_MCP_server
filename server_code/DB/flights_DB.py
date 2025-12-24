# DB/flights_DB.py
from datetime import date, time, datetime, timedelta
import uuid
from schemas.Flight1 import Flight

mock_flights = {}
mock_Booking = {}

def generate_mock_flights():
    global mock_flights
    today = date.today()
    tomorrow = today + timedelta(days=1)
    day_after_tomorrow = today + timedelta(days=2)

    flights_data = [
        {
            "flight_id": str(uuid.uuid4()),
            "airline": "AirSwift",
            "flight_number": "AS101",
            "origin": "NYC",
            "destination": "LAX",
            "departure_time": datetime.combine(tomorrow, time(9, 0)),
            "arrival_time": datetime.combine(tomorrow, time(12, 30)),
            "price": 250.00,
            "available_seats": 100
        },
        {
            "flight_id": str(uuid.uuid4()),
            "airline": "Global Airlines",
            "flight_number": "GA202",
            "origin": "LAX",
            "destination": "NYC",
            "departure_time": datetime.combine(tomorrow, time(14, 0)),
            "arrival_time": datetime.combine(tomorrow, time(17, 30)),
            "price": 230.00,
            "available_seats": 80
        },
        {
            "flight_id": str(uuid.uuid4()),
            "airline": "AirSwift",
            "flight_number": "AS102",
            "origin": "NYC",
            "destination": "LAX",
            "departure_time": datetime.combine(day_after_tomorrow, time(10, 0)),
            "arrival_time": datetime.combine(day_after_tomorrow, time(13, 30)),
            "price": 270.00,
            "available_seats": 120
        },
        {
            "flight_id": str(uuid.uuid4()),
            "airline": "SkyConnect",
            "flight_number": "SC303",
            "origin": "SFO",
            "destination": "ORD",
            "departure_time": datetime.combine(tomorrow, time(8, 0)),
            "arrival_time": datetime.combine(tomorrow, time(11, 0)),
            "price": 180.00,
            "available_seats": 50
        }
    ]

    for data in flights_data:
        flight = Flight(**data)
        mock_flights[flight.flight_id] = flight

    return mock_flights.copy()

# Ensure data is generated
generate_mock_flights()