# How to Add MCP Server to Google AI Studio (Gemini)

## Method 1: Using the UI (Recommended)

1. **Look for MCP Settings in the IDE:**
   - Check the Settings/Preferences menu
   - Look for "MCP Servers" or "Model Context Protocol" section
   - Or look for a gear icon ⚙️ in the IDE interface

2. **Add the Flight Booking Server:**
   - Click "Add MCP Server" or similar button
   - Enter the following details:
     - **Server Name:** `flights-booking-server`
     - **Command:** `d:\LLmLangchain\FlightsBookingAgent\flights_booking_server\.venv\Scripts\python.exe`
     - **Arguments:** `d:\LLmLangchain\FlightsBookingAgent\flights_booking_server\server_code\run_mcp_server.py`

3. **Save and Restart** (if required)

## Method 2: Manual Configuration File Edit

If you need to manually edit the MCP configuration:

1. **Locate the config file:**
   - Path: `C:\Users\venky\.gemini\antigravity\mcp_config.json`

2. **Add this configuration:**
   ```json
   {
     "mcpServers": {
       "flights-booking-server": {
         "command": "d:\\LLmLangchain\\FlightsBookingAgent\\flights_booking_server\\.venv\\Scripts\\python.exe",
         "args": [
           "d:\\LLmLangchain\\FlightsBookingAgent\\flights_booking_server\\server_code\\run_mcp_server.py"
         ]
       }
     }
   }
   ```

3. **If there are existing servers**, merge them like this:
   ```json
   {
     "mcpServers": {
       "existing-server": {
         "command": "...",
         "args": ["..."]
       },
       "flights-booking-server": {
         "command": "d:\\LLmLangchain\\FlightsBookingAgent\\flights_booking_server\\.venv\\Scripts\\python.exe",
         "args": [
           "d:\\LLmLangchain\\FlightsBookingAgent\\flights_booking_server\\server_code\\run_mcp_server.py"
         ]
       }
     }
   }
   ```

4. **Restart the IDE** to load the new configuration

## Method 3: Copy the Config File

You can copy the prepared configuration file:

```powershell
# Backup existing config (if it exists)
Copy-Item "C:\Users\venky\.gemini\antigravity\mcp_config.json" "C:\Users\venky\.gemini\antigravity\mcp_config.json.backup" -ErrorAction SilentlyContinue

# Copy the new config
Copy-Item "d:\LLmLangchain\FlightsBookingAgent\flights_booking_server\gemini_mcp_config.json" "C:\Users\venky\.gemini\antigravity\mcp_config.json"
```

**⚠️ Warning:** This will overwrite any existing MCP server configurations!

## Verifying the Connection

After adding the server, you should be able to:

1. **See the server listed** in the MCP servers panel
2. **Use the `list_resources` tool** to query it:
   ```
   list_resources("flights-booking-server")
   ```
3. **Ask natural language queries** like:
   - "What airports are available in the flight booking system?"
   - "Show me all flights"
   - "Search for flights from NYC to LAX"

## Troubleshooting

### Server Not Appearing
- Restart the IDE completely
- Check that Python path is correct: `d:\LLmLangchain\FlightsBookingAgent\flights_booking_server\.venv\Scripts\python.exe`
- Verify the server runs manually:
  ```powershell
  cd d:\LLmLangchain\FlightsBookingAgent\flights_booking_server\server_code
  python run_mcp_server.py
  ```

### Connection Errors
- Check the IDE's error logs
- Ensure all dependencies are installed in the virtual environment
- Try using system Python instead of venv Python:
  ```json
  "command": "python"
  ```

## Alternative: Use the Test Client

If IDE integration doesn't work, you can still interact with the MCP server using the test client:

```powershell
cd d:\LLmLangchain\FlightsBookingAgent\flights_booking_server
python client_code\interactive_demo.py
```

This will demonstrate all the server's capabilities without IDE integration.
