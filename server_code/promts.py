# prompts.py
from mcp_instance import mcp

@mcp.prompt(description="Prompt for searching flights using the tool and summarizing results.")
async def flight_search_prompt(origin: str, destination: str, date: str, passenger: int = 1) -> str:
    return (
        f"The user wants to find flights from {origin} to {destination} on {date} for {passenger} passenger(s). "
        "Use the 'search_flights' tool to retrieve available flights and summarize the options for the user. "
        "If no flights are found, politely inform the user."
    )

@mcp.prompt(description="Prompt for booking a flight using the tool and confirming the booking.")
async def flight_booking_prompt(flight_id: str, passenger_name: str, num_seats: int) -> str:
    return (
        f"The user wants to book {num_seats} seat(s) on flight {flight_id} for passenger {passenger_name}. "
        "Use the 'book_flight' tool to make the booking and confirm the details to the user."
    )

@mcp.prompt(description="Prompt for cancelling a booking using the tool and confirming cancellation.")
async def booking_cancel_prompt(booking_id: str) -> str:
    return (
        f"The user wants to cancel the booking with ID {booking_id}. "
        "Use the 'cancel_booking' tool to process the cancellation and inform the user of the result."
    )

@mcp.prompt(description="Prompt for showing flight details using the tool.")
async def flight_details_prompt(flight_id: str) -> str:
    return (
        f"The user requested details for flight {flight_id}. "
        "Use the 'flight_details' tool to retrieve and present the flight information."
    )

@mcp.prompt()
async def handle_disruption(flight_id: str, reason: str) -> str:
    return f"""A passenger's flight {flight_id} has been disrupted due to: {reason}

Please help resolve this by:
1. Understanding the passenger's situation
2. Finding alternative flight options using search_flights
3. Providing clear rebooking steps
4. Offering appropriate compensation if applicable

Be empathetic and solution-focused in your response."""