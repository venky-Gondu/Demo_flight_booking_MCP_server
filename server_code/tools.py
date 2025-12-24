# tools.py
from mcp_instance import mcp
from DB.flights_DB import mock_flights, mock_Booking
from schemas.Flight1 import Bookings
from typing import List, Dict, Any
from datetime import datetime
import uuid

@mcp.tool(description="Search for flights by origin, destination, and date.")
async def search_flights(origin: str, destination: str, departure_date: str, passenger: int = 1) -> List[Dict[str, Any]]:
    try:
        parsed_date = datetime.fromisoformat(departure_date).date()
    except ValueError:
        return [{"error": "Invalid date format. Use YYYY-MM-DD."}]

    results = []
    for flight in mock_flights.values():
        if (
            flight.origin.lower() == origin.lower()
            and flight.destination.lower() == destination.lower()
            and flight.departure_time.date() == parsed_date
            and flight.available_seats >= passenger
        ):
            results.append(flight.dict())

    return results


@mcp.tool(description="Book a flight for a passenger.")
async def book_flight(flight_id: str, passenger_name: str, num_seats: int) -> Dict[str, Any]:
    flight = mock_flights.get(flight_id)
    if not flight:
        return {"error": "Flight not found."}
    if flight.available_seats < num_seats:
        return {"error": "Not enough available seats."}

    flight.available_seats -= num_seats
    booking_id = str(uuid.uuid4())
    new_booking = Bookings(
        booking_id=booking_id,
        flight_id=flight_id,
        passenger_name=passenger_name,
        num_seats=num_seats,
        booking_time=datetime.now(),
        status="confirmed"
    )
    mock_Booking[booking_id] = new_booking
    return new_booking.dict()


@mcp.tool(description="Cancel an existing booking.")
async def cancel_booking(booking_id: str) -> Dict[str, Any]:
    booking = mock_Booking.get(booking_id)
    if not booking:
        return {"error": "Booking not found."}

    flight = mock_flights.get(booking.flight_id)
    if not flight:
        return {"error": "Flight not found for this booking."}

    flight.available_seats += booking.num_seats
    cancelled = mock_Booking.pop(booking_id)
    return {"status": "cancelled", "booking": cancelled.dict()}