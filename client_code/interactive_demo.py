"""
Interactive MCP Server Demo
This script demonstrates the MCP server functionality with sample queries
"""
import asyncio
import sys
import os
import json
from datetime import date, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'server_code'))

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class FlightBookingDemo:
    def __init__(self):
        self.session = None
        self.booking_ids = []
        
    async def connect(self):
        """Connect to the MCP server"""
        server_params = StdioServerParameters(
            command="python",
            args=[os.path.join(os.path.dirname(__file__), "..", "server_code", "run_mcp_server.py")],
            env=None
        )
        
        self.client = stdio_client(server_params)
        self.read, self.write = await self.client.__aenter__()
        self.session = ClientSession(self.read, self.write)
        await self.session.__aenter__()
        await self.session.initialize()
        
    async def disconnect(self):
        """Disconnect from the MCP server"""
        if self.session:
            await self.session.__aexit__(None, None, None)
        if self.client:
            await self.client.__aexit__(None, None, None)
    
    async def query_airports(self):
        """Query: What airports are available?"""
        print("\n" + "="*70)
        print("QUERY: What airports are available?")
        print("="*70)
        
        result = await self.session.read_resource("file://airports")
        airports = json.loads(result.contents[0].text)
        
        print("\nAvailable Airports:")
        for airport in airports:
            print(f"   • {airport}")
        
        return airports
    
    async def query_all_flights(self):
        """Query: Show me all available flights"""
        print("\n" + "="*70)
        print("QUERY: Show me all available flights")
        print("="*70)
        
        result = await self.session.read_resource("file://flights")
        flights = json.loads(result.contents[0].text)
        
        print(f"\nTotal Flights Available: {len(flights)}\n")
        
        for flight_id, flight in flights.items():
            print(f"  Flight {flight['flight_number']} - {flight['airline']}")
            print(f"     Route: {flight['origin']} → {flight['destination']}")
            print(f"     Departure: {flight['departure_time']}")
            print(f"     Price: ${flight['price']} | Seats: {flight['available_seats']}")
            print()
        
        return flights
    
    async def query_search_flights(self, origin, destination, passengers=2):
        """Query: Find flights from NYC to LAX tomorrow for 2 passengers"""
        tomorrow = (date.today() + timedelta(days=1)).isoformat()
        
        print("\n" + "="*70)
        print(f"QUERY: Find flights from {origin} to {destination} tomorrow for {passengers} passengers")
        print("="*70)
        
        result = await self.session.call_tool(
            "search_flights",
            arguments={
                "origin": origin,
                "destination": destination,
                "departure_date": tomorrow,
                "passenger": passengers
            }
        )
        
        # Parse the result - it's a list of TextContent objects
        flights_json = result.content[0].text
        flights = json.loads(flights_json)
        
        if isinstance(flights, list) and len(flights) > 0:
            if 'error' in flights[0]:
                print(f"\nERROR: {flights[0]['error']}")
                return []
            
            print(f"\nFound {len(flights)} flight(s):\n")
            for flight in flights:
                print(f"  Flight {flight['flight_number']} - {flight['airline']}")
                print(f"     Route: {flight['origin']} → {flight['destination']}")
                print(f"     Departure: {flight['departure_time']}")
                print(f"     Price: ${flight['price']} | Available Seats: {flight['available_seats']}")
                print(f"     Flight ID: {flight['flight_id']}")
                print()
            
            return flights
        else:
            print("\nNo flights found matching your criteria")
            return []
    
    async def query_book_flight(self, flight_id, passenger_name, num_seats):
        """Query: Book a flight"""
        print("\n" + "="*70)
        print(f"QUERY: Book {num_seats} seat(s) on flight for {passenger_name}")
        print("="*70)
        
        result = await self.session.call_tool(
            "book_flight",
            arguments={
                "flight_id": flight_id,
                "passenger_name": passenger_name,
                "num_seats": num_seats
            }
        )
        
        booking_json = result.content[0].text
        booking = json.loads(booking_json)
        
        if 'error' in booking:
            print(f"\nBooking Failed: {booking['error']}")
            return None
        
        print("\nBooking Confirmed!")
        print(f"   Booking ID: {booking['booking_id']}")
        print(f"   Flight ID: {booking['flight_id']}")
        print(f"   Passenger: {booking['passenger_name']}")
        print(f"   Seats: {booking['num_seats']}")
        print(f"   Status: {booking['status']}")
        print(f"   Booking Time: {booking['booking_time']}")
        
        self.booking_ids.append(booking['booking_id'])
        return booking
    
    async def query_cancel_booking(self, booking_id):
        """Query: Cancel a booking"""
        print("\n" + "="*70)
        print(f"QUERY: Cancel booking {booking_id}")
        print("="*70)
        
        result = await self.session.call_tool(
            "cancel_booking",
            arguments={
                "booking_id": booking_id
            }
        )
        
        cancel_json = result.content[0].text
        cancel_result = json.loads(cancel_json)
        
        if 'error' in cancel_result:
            print(f"\nCancellation Failed: {cancel_result['error']}")
            return None
        
        print("\nBooking Cancelled Successfully!")
        print(f"   Status: {cancel_result['status']}")
        print(f"   Cancelled Booking Details:")
        print(f"      Booking ID: {cancel_result['booking']['booking_id']}")
        print(f"      Passenger: {cancel_result['booking']['passenger_name']}")
        print(f"      Seats Refunded: {cancel_result['booking']['num_seats']}")
        
        return cancel_result

async def main():
    """Run the demo"""
    demo = FlightBookingDemo()
    
    print("\n" + "=" * 70)
    print("   FLIGHT BOOKING MCP SERVER - INTERACTIVE DEMO")
    print("=" * 70)
    
    try:
        # Connect to server
        print("\nConnecting to MCP Server...")
        await demo.connect()
        print("Connected successfully!")
        
        # Demo 1: List airports
        await demo.query_airports()
        
        # Demo 2: List all flights
        flights = await demo.query_all_flights()
        
        # Demo 3: Search for specific flights
        search_results = await demo.query_search_flights("NYC", "LAX", 2)
        
        # Demo 4: Book a flight
        if search_results:
            flight_to_book = search_results[0]
            booking = await demo.query_book_flight(
                flight_to_book['flight_id'],
                "Alice Johnson",
                2
            )
            
            # Demo 5: Cancel the booking
            if booking:
                await asyncio.sleep(1)  # Small delay for demonstration
                await demo.query_cancel_booking(booking['booking_id'])
        
        print("\n" + "="*70)
        print("DEMO COMPLETED SUCCESSFULLY!")
        print("="*70)
        print("\nThe MCP server is working correctly and ready to use!")
        print("See MCP_CONNECTION_GUIDE.md for instructions on connecting to the IDE.")
        
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await demo.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
