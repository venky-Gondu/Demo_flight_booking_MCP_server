"""
Test client to interact with the Flight Booking MCP Server
"""
import asyncio
import sys
import os

# Add the server_code directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'server_code'))

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_mcp_server():
    """Test the MCP server by listing resources and calling tools"""
    
    # Server parameters
    server_params = StdioServerParameters(
        command="python",
        args=[os.path.join(os.path.dirname(__file__), "..", "server_code", "run_mcp_server.py")],
        env=None
    )
    
    print("=" * 60)
    print("Testing Flight Booking MCP Server")
    print("=" * 60)
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()
            
            print("\n✓ Server connected successfully!\n")
            
            # List available resources
            print("📋 Available Resources:")
            print("-" * 60)
            resources = await session.list_resources()
            for resource in resources.resources:
                print(f"  • {resource.uri}")
                if resource.description:
                    print(f"    Description: {resource.description}")
            
            # List available tools
            print("\n🔧 Available Tools:")
            print("-" * 60)
            tools = await session.list_tools()
            for tool in tools.tools:
                print(f"  • {tool.name}")
                if tool.description:
                    print(f"    Description: {tool.description}")
            
            # List available prompts
            print("\n💬 Available Prompts:")
            print("-" * 60)
            prompts = await session.list_prompts()
            for prompt in prompts.prompts:
                print(f"  • {prompt.name}")
                if prompt.description:
                    print(f"    Description: {prompt.description}")
            
            # Test 1: Read airports resource
            print("\n" + "=" * 60)
            print("TEST 1: Reading Available Airports")
            print("=" * 60)
            try:
                airports_result = await session.read_resource("file://airports")
                print("✓ Success!")
                print(f"Available Airports: {airports_result.contents[0].text}")
            except Exception as e:
                print(f"✗ Error: {e}")
            
            # Test 2: Read all flights resource
            print("\n" + "=" * 60)
            print("TEST 2: Reading All Flights")
            print("=" * 60)
            try:
                flights_result = await session.read_resource("file://flights")
                print("✓ Success!")
                import json
                flights_data = json.loads(flights_result.contents[0].text)
                print(f"Total flights available: {len(flights_data)}")
                for flight_id, flight in flights_data.items():
                    print(f"\n  Flight {flight['flight_number']}:")
                    print(f"    Route: {flight['origin']} → {flight['destination']}")
                    print(f"    Airline: {flight['airline']}")
                    print(f"    Price: ${flight['price']}")
                    print(f"    Available Seats: {flight['available_seats']}")
            except Exception as e:
                print(f"✗ Error: {e}")
            
            # Test 3: Search for flights using tool
            print("\n" + "=" * 60)
            print("TEST 3: Searching Flights (NYC to LAX)")
            print("=" * 60)
            try:
                from datetime import date, timedelta
                tomorrow = (date.today() + timedelta(days=1)).isoformat()
                
                search_result = await session.call_tool(
                    "search_flights",
                    arguments={
                        "origin": "NYC",
                        "destination": "LAX",
                        "departure_date": tomorrow,
                        "passenger": 2
                    }
                )
                print("✓ Success!")
                import json
                search_data = json.loads(search_result.content[0].text)
                print(f"Found {len(search_data)} flights:")
                for flight in search_data:
                    print(f"\n  Flight {flight['flight_number']}:")
                    print(f"    Airline: {flight['airline']}")
                    print(f"    Departure: {flight['departure_time']}")
                    print(f"    Price: ${flight['price']}")
                    print(f"    Available Seats: {flight['available_seats']}")
            except Exception as e:
                print(f"✗ Error: {e}")
            
            # Test 4: Book a flight
            print("\n" + "=" * 60)
            print("TEST 4: Booking a Flight")
            print("=" * 60)
            try:
                # First get a flight ID
                flights_result = await session.read_resource("file://flights")
                import json
                flights_data = json.loads(flights_result.contents[0].text)
                first_flight_id = list(flights_data.keys())[0]
                
                booking_result = await session.call_tool(
                    "book_flight",
                    arguments={
                        "flight_id": first_flight_id,
                        "passenger_name": "John Doe",
                        "num_seats": 2
                    }
                )
                print("✓ Success!")
                booking_data = json.loads(booking_result.content[0].text)
                print(f"Booking confirmed!")
                print(f"  Booking ID: {booking_data['booking_id']}")
                print(f"  Passenger: {booking_data['passenger_name']}")
                print(f"  Seats: {booking_data['num_seats']}")
                print(f"  Status: {booking_data['status']}")
                
                # Save booking ID for cancellation test
                booking_id = booking_data['booking_id']
                
                # Test 5: Cancel the booking
                print("\n" + "=" * 60)
                print("TEST 5: Cancelling the Booking")
                print("=" * 60)
                cancel_result = await session.call_tool(
                    "cancel_booking",
                    arguments={
                        "booking_id": booking_id
                    }
                )
                print("✓ Success!")
                cancel_data = json.loads(cancel_result.content[0].text)
                print(f"Booking cancelled!")
                print(f"  Status: {cancel_data['status']}")
                
            except Exception as e:
                print(f"✗ Error: {e}")
            
            print("\n" + "=" * 60)
            print("All tests completed!")
            print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_mcp_server())
