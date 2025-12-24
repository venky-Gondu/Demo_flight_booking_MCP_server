# ✈️ Flight Booking MCP Server

A **Model Context Protocol (MCP)** server for flight booking operations. This server provides tools, resources, and prompts for searching flights, booking seats, and managing reservations through AI assistants like Claude, Gemini, and other MCP-compatible clients.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-1.12.2+-green.svg)](https://github.com/anthropics/mcp)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 🌟 Features

- **🔍 Flight Search** - Search flights by origin, destination, and date
- **🎫 Booking Management** - Book and cancel flight reservations
- **📋 Resource Access** - Query available flights and airports
- **💬 AI Prompts** - Pre-built prompts for common flight operations
- **🗄️ Mock Database** - In-memory flight data for testing

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [MCP Integration](#mcp-integration)
- [API Reference](#api-reference)
- [Usage Examples](#usage-examples)
- [Development](#development)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)

## 🚀 Installation

### Prerequisites

- Python 3.10 or higher
- pip or uv package manager

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/venky-Gondu/Demo_flight_booking_MCP_server.git
   cd Demo_flight_booking_MCP_server
   ```

2. **Create and activate virtual environment:**
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # Linux/Mac
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## ⚡ Quick Start

### Running the Server

```bash
cd server_code
python run_mcp_server.py
```

### Testing with Demo Client

```bash
python client_code/interactive_demo.py
```

This will run a comprehensive demo showing all server capabilities.

## 🔌 MCP Integration

### Google AI Studio (Gemini)

1. **Copy configuration:**
   ```powershell
   Copy-Item "gemini_mcp_config.json" "$env:USERPROFILE\.gemini\antigravity\mcp_config.json"
   ```

2. **Restart Google AI Studio**

3. **Test the connection:**
   ```
   Ask: "What airports are available in the flight booking system?"
   ```

### Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "flights-booking-server": {
      "command": "python",
      "args": ["path/to/server_code/run_mcp_server.py"]
    }
  }
}
```

### Other MCP Clients

See [MCP_CONNECTION_GUIDE.md](MCP_CONNECTION_GUIDE.md) for detailed integration instructions.

## 📚 API Reference

### Resources

#### `file://flights`
Returns all available flights with complete details.

**Response:**
```json
{
  "flight_id": {
    "flight_id": "uuid",
    "airline": "AirSwift",
    "flight_number": "AS101",
    "origin": "NYC",
    "destination": "LAX",
    "departure_time": "2025-12-25T09:00:00",
    "arrival_time": "2025-12-25T12:30:00",
    "price": 250.0,
    "available_seats": 100
  }
}
```

#### `file://airports`
Returns list of supported airports.

**Response:**
```json
["NYC", "LAX", "SFO", "ORD", "DFW", "ATL", "DEN"]
```

### Tools

#### `search_flights`
Search for flights matching criteria.

**Parameters:**
- `origin` (string, required) - Departure airport code
- `destination` (string, required) - Arrival airport code
- `departure_date` (string, required) - Date in YYYY-MM-DD format
- `passenger` (integer, optional) - Number of passengers (default: 1)

**Example:**
```python
search_flights(
    origin="NYC",
    destination="LAX",
    departure_date="2025-12-25",
    passenger=2
)
```

#### `book_flight`
Book seats on a flight.

**Parameters:**
- `flight_id` (string, required) - Flight identifier
- `passenger_name` (string, required) - Name of passenger
- `num_seats` (integer, required) - Number of seats to book

**Returns:**
```json
{
  "booking_id": "uuid",
  "flight_id": "uuid",
  "passenger_name": "John Doe",
  "num_seats": 2,
  "booking_time": "2025-12-24T10:00:00",
  "status": "confirmed"
}
```

#### `cancel_booking`
Cancel an existing booking.

**Parameters:**
- `booking_id` (string, required) - Booking identifier

**Returns:**
```json
{
  "status": "cancelled",
  "booking": { /* booking details */ }
}
```

### Prompts

- `flight_search_prompt` - Guided flight search
- `flight_booking_prompt` - Guided booking process
- `booking_cancel_prompt` - Guided cancellation
- `flight_details_prompt` - View flight details
- `handle_disruption` - Handle flight disruptions

## 💡 Usage Examples

### Example 1: Search and Book

```python
# Search for flights
flights = await search_flights(
    origin="NYC",
    destination="LAX",
    departure_date="2025-12-25",
    passenger=2
)

# Book the first available flight
booking = await book_flight(
    flight_id=flights[0]['flight_id'],
    passenger_name="Alice Johnson",
    num_seats=2
)

print(f"Booking confirmed: {booking['booking_id']}")
```

### Example 2: Natural Language (via MCP Client)

```
User: "Find me flights from NYC to LAX tomorrow for 2 people"
AI: [Uses search_flights tool and presents results]

User: "Book 2 seats on the AirSwift flight for John Smith"
AI: [Uses book_flight tool and confirms booking]
```

## 🛠️ Development

### Project Structure

```
flights_booking_server/
├── server_code/
│   ├── DB/
│   │   └── flights_DB.py      # Mock flight database
│   ├── schemas/
│   │   └── Flight1.py          # Pydantic models
│   ├── mcp_instance.py         # MCP server instance
│   ├── tools.py                # MCP tools implementation
│   ├── resources.py            # MCP resources
│   ├── promts.py               # MCP prompts
│   └── run_mcp_server.py       # Server entry point
├── client_code/
│   ├── interactive_demo.py     # Full feature demo
│   ├── simple_test.py          # Basic connectivity test
│   └── test_mcp_client.py      # Comprehensive tests
├── pyproject.toml              # Project metadata
├── requirements.txt            # Dependencies
└── README.md                   # This file
```

### Adding New Features

1. **Add a new tool:**
   - Define function in `server_code/tools.py`
   - Decorate with `@mcp.tool(description="...")`

2. **Add a new resource:**
   - Define function in `server_code/resources.py`
   - Decorate with `@mcp.resource("file://resource_name")`

3. **Add a new prompt:**
   - Define function in `server_code/promts.py`
   - Decorate with `@mcp.prompt(description="...")`

## 🧪 Testing

### Run All Tests

```bash
python client_code/interactive_demo.py
```

### Run Specific Tests

```bash
# Test connectivity only
python client_code/simple_test.py

# View test results
cat client_code/test_results.txt
```

### Expected Output

See [TEST_RESULTS.md](TEST_RESULTS.md) for detailed test output examples.

## 🐛 Troubleshooting

### Server Won't Start

**Issue:** `ModuleNotFoundError: No module named 'mcp'`

**Solution:**
```bash
pip install mcp[cli]
```

### MCP Client Can't Connect

**Issue:** Server not found in MCP client

**Solutions:**
1. Verify configuration file location
2. Restart the MCP client application
3. Check Python path in configuration
4. Review [GEMINI_MCP_SETUP.md](GEMINI_MCP_SETUP.md)

### No Flights Found

**Issue:** Search returns empty results

**Cause:** Flight dates are dynamically generated (tomorrow and day after)

**Solution:** Use tomorrow's date or check available flights:
```python
# Get all flights to see available dates
flights = await read_resource("file://flights")
```

## 📖 Documentation

- [TEST_RESULTS.md](TEST_RESULTS.md) - Complete test results
- [MCP_CONNECTION_GUIDE.md](MCP_CONNECTION_GUIDE.md) - General MCP setup
- [GEMINI_MCP_SETUP.md](GEMINI_MCP_SETUP.md) - Gemini-specific setup
- [FINAL_SETUP_SUMMARY.md](FINAL_SETUP_SUMMARY.md) - Quick setup summary

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [FastMCP](https://github.com/jlowin/fastmcp)
- Model Context Protocol by [Anthropic](https://github.com/anthropics/mcp)
- Tested with Google AI Studio (Gemini)

## 📧 Contact

Venky Gondu - [@venky-Gondu](https://github.com/venky-Gondu)

Project Link: [https://github.com/venky-Gondu/Demo_flight_booking_MCP_server](https://github.com/venky-Gondu/Demo_flight_booking_MCP_server)

---

**⭐ If you find this project useful, please consider giving it a star!**
