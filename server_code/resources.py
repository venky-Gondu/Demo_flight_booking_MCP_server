# resources.py
from mcp_instance import mcp
from DB.flights_DB import mock_flights

@mcp.resource("file://flights")
async def total_flights() -> dict:
    return {fid: flight.dict() for fid, flight in mock_flights.items()}

@mcp.resource("file://flight_details/{flight_id}")
async def flight_details(flight_id: str) -> dict:
    flight = mock_flights.get(flight_id)
    return flight.dict() if flight else {"error": "Flight not found."}

@mcp.resource("file://airports")
async def available_airports() -> list[str]:
    return ["NYC", "LAX", "SFO", "ORD", "DFW", "ATL", "DEN"]