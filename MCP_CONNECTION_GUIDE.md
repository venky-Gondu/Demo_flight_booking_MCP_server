# Flight Booking MCP Server - Connection Guide

## ✅ Server Status: WORKING!

The MCP server has been tested and is functioning correctly. See `client_code/test_results.txt` for test results.

## 🔌 Connecting to Google AI Studio (This IDE)

To connect this MCP server to Google AI Studio, you need to configure it in the MCP settings.

### Option 1: Using MCP Configuration File

1. **Locate your MCP configuration directory:**
   - Windows: `%APPDATA%\Code\User\globalStorage\saoudrizwan.claude-dev\settings\`
   - Or check the IDE's MCP settings panel

2. **Create or edit `mcp_settings.json`:**

```json
{
  "mcpServers": {
    "flights-booking-server": {
      "command": "python",
      "args": [
        "d:\\LLmLangchain\\FlightsBookingAgent\\flights_booking_server\\server_code\\run_mcp_server.py"
      ],
      "cwd": "d:\\LLmLangchain\\FlightsBookingAgent\\flights_booking_server\\server_code",
      "env": {}
    }
  }
}
```

3. **Restart the IDE** to load the new MCP server configuration.

### Option 2: Using the IDE's MCP Settings Panel

1. Open the MCP settings panel in the IDE
2. Add a new MCP server with these details:
   - **Name:** `flights-booking-server`
   - **Command:** `python`
   - **Args:** `d:\LLmLangchain\FlightsBookingAgent\flights_booking_server\server_code\run_mcp_server.py`
   - **Working Directory:** `d:\LLmLangchain\FlightsBookingAgent\flights_booking_server\server_code`

### Option 3: Using Virtual Environment (Recommended)

If you want to use the virtual environment:

```json
{
  "mcpServers": {
    "flights-booking-server": {
      "command": "d:\\LLmLangchain\\FlightsBookingAgent\\flights_booking_server\\.venv\\Scripts\\python.exe",
      "args": [
        "d:\\LLmLangchain\\FlightsBookingAgent\\flights_booking_server\\server_code\\run_mcp_server.py"
      ],
      "cwd": "d:\\LLmLangchain\\FlightsBookingAgent\\flights_booking_server\\server_code",
      "env": {}
    }
  }
}
```

## 📋 Available Features

Once connected, you'll have access to:

### Resources:
- `file://flights/` - List all available flights
- `file://airports/` - List all available airports

### Tools:
- `search_flights` - Search for flights by origin, destination, and date
- `book_flight` - Book a flight for a passenger
- `cancel_booking` - Cancel an existing booking

### Prompts:
- `flight_search_prompt` - Prompt for searching flights
- `flight_booking_prompt` - Prompt for booking a flight
- `booking_cancel_prompt` - Prompt for cancelling a booking
- `flight_details_prompt` - Prompt for showing flight details
- `handle_disruption` - Handle flight disruptions

## 🧪 Testing the Connection

After connecting, try these queries:

1. **List available airports:**
   ```
   Show me all available airports
   ```

2. **Search for flights:**
   ```
   Find me flights from NYC to LAX tomorrow for 2 passengers
   ```

3. **Book a flight:**
   ```
   Book 2 seats on flight AS101 for John Doe
   ```

## 🐛 Troubleshooting

If you encounter issues:

1. **Check Python is in PATH:**
   ```powershell
   python --version
   ```

2. **Verify the server runs manually:**
   ```powershell
   cd d:\LLmLangchain\FlightsBookingAgent\flights_booking_server\server_code
   python run_mcp_server.py
   ```

3. **Check the test results:**
   ```powershell
   python client_code\simple_test.py
   cat client_code\test_results.txt
   ```

4. **Verify dependencies are installed:**
   ```powershell
   .venv\Scripts\Activate.ps1
   pip list | findstr mcp
   ```

## 📝 Notes

- The server uses mock data stored in `server_code/DB/flights_DB.py`
- Flight dates are dynamically generated (tomorrow and day after tomorrow)
- Available airports: NYC, LAX, SFO, ORD, DFW, ATL, DEN
