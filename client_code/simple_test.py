"""
Simple test client to interact with the Flight Booking MCP Server
"""
import asyncio
import sys
import os
import json
from datetime import date, timedelta

# Add the server_code directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'server_code'))

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_mcp_server():
    """Test the MCP server by listing resources and calling tools"""
    
    output = []
    
    # Server parameters
    server_params = StdioServerParameters(
        command="python",
        args=[os.path.join(os.path.dirname(__file__), "..", "server_code", "run_mcp_server.py")],
        env=None
    )
    
    output.append("=" * 60)
    output.append("Testing Flight Booking MCP Server")
    output.append("=" * 60)
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the session
                await session.initialize()
                
                output.append("\n✓ Server connected successfully!\n")
                
                # List available resources
                output.append("📋 Available Resources:")
                output.append("-" * 60)
                resources = await session.list_resources()
                for resource in resources.resources:
                    output.append(f"  • {resource.uri}")
                    if resource.description:
                        output.append(f"    Description: {resource.description}")
                
                # List available tools
                output.append("\n🔧 Available Tools:")
                output.append("-" * 60)
                tools = await session.list_tools()
                for tool in tools.tools:
                    output.append(f"  • {tool.name}")
                    if tool.description:
                        output.append(f"    Description: {tool.description}")
                
                # List available prompts
                output.append("\n💬 Available Prompts:")
                output.append("-" * 60)
                prompts = await session.list_prompts()
                for prompt in prompts.prompts:
                    output.append(f"  • {prompt.name}")
                    if prompt.description:
                        output.append(f"    Description: {prompt.description}")
                
                # Test 1: Read airports resource
                output.append("\n" + "=" * 60)
                output.append("TEST 1: Reading Available Airports")
                output.append("=" * 60)
                try:
                    airports_result = await session.read_resource("file://airports")
                    output.append("✓ Success!")
                    output.append(f"Available Airports: {airports_result.contents[0].text}")
                except Exception as e:
                    output.append(f"✗ Error: {e}")
                
                # Test 2: Search for flights using tool
                output.append("\n" + "=" * 60)
                output.append("TEST 2: Searching Flights (NYC to LAX)")
                output.append("=" * 60)
                try:
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
                    output.append("✓ Success!")
                    search_data = json.loads(search_result.content[0].text)
                    output.append(f"Found {len(search_data)} flights:")
                    for flight in search_data:
                        output.append(f"\n  Flight {flight['flight_number']}:")
                        output.append(f"    Airline: {flight['airline']}")
                        output.append(f"    Departure: {flight['departure_time']}")
                        output.append(f"    Price: ${flight['price']}")
                        output.append(f"    Available Seats: {flight['available_seats']}")
                except Exception as e:
                    output.append(f"✗ Error: {e}")
                
                output.append("\n" + "=" * 60)
                output.append("All tests completed successfully!")
                output.append("=" * 60)
                
    except Exception as e:
        output.append(f"\n✗ FATAL ERROR: {e}")
        import traceback
        output.append(traceback.format_exc())
    
    # Write output to file
    output_file = os.path.join(os.path.dirname(__file__), "test_results.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(output))
    
    # Also print to console
    print("\n".join(output))
    print(f"\n\nResults saved to: {output_file}")

if __name__ == "__main__":
    asyncio.run(test_mcp_server())
