# MCP Server - Tools Reference

## What Are Tools?

**Tools** are functions that AI models can actively call to perform actions. The LLM decides when to use tools based on context.

### Protocol Operations

```
tools/list → Discover available tools
tools/call → Execute a specific tool
```

## Tool Definition Structure

Every tool consists of:

1. **Name**: Unique identifier (e.g., `search_flights`)
2. **Description**: What the tool does
3. **Input Schema**: JSON Schema defining parameters
4. **Implementation**: Function that executes the tool

## Python Implementation (FastMCP)

### Basic Tool

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-server")

@mcp.tool()
async def search_flights(origin: str, destination: str, date: str) -> str:
    """Search for available flights.

    Args:
        origin: Departure city code (e.g., SFO)
        destination: Arrival city code (e.g., LAX)
        date: Travel date (YYYY-MM-DD format)
    """
    # Implementation
    return f"Flights from {origin} to {destination} on {date}"
```

### Tool with Complex Types

```python
from typing import List, Optional
from pydantic import BaseModel

class FlightPreferences(BaseModel):
    max_stops: int = 0
    preferred_airlines: Optional[List[str]] = None
    class_preference: str = "economy"

@mcp.tool()
async def search_flights_advanced(
    origin: str,
    destination: str,
    date: str,
    preferences: FlightPreferences
) -> str:
    """Search flights with preferences."""
    airlines = preferences.preferred_airlines or ["any"]
    return f"Searching flights with max {preferences.max_stops} stops"
```

### Error Handling

```python
@mcp.tool()
async def book_flight(flight_id: str, passenger_name: str) -> str:
    """Book a flight."""
    try:
        # Attempt booking
        result = await booking_api.book(flight_id, passenger_name)
        return f"Flight {flight_id} booked for {passenger_name}"
    except BookingError as e:
        return f"Booking failed: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"
```

## TypeScript Implementation

### Basic Tool

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { ListToolsRequestSchema, CallToolRequestSchema } from "@modelcontextprotocol/sdk/types.js";

const server = new Server({ name: "my-server", version: "1.0.0" });

// List tools
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "search_flights",
      description: "Search for available flights",
      inputSchema: {
        type: "object",
        properties: {
          origin: {
            type: "string",
            description: "Departure city code"
          },
          destination: {
            type: "string",
            description: "Arrival city code"
          },
          date: {
            type: "string",
            format: "date",
            description: "Travel date (YYYY-MM-DD)"
          }
        },
        required: ["origin", "destination", "date"]
      }
    }
  ]
}));

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  if (name === "search_flights") {
    const { origin, destination, date } = args as {
      origin: string;
      destination: string;
      date: string;
    };

    const results = await searchFlights(origin, destination, date);

    return {
      content: [
        {
          type: "text",
          text: `Found ${results.length} flights`
        }
      ]
    };
  }

  throw new Error(`Unknown tool: ${name}`);
});
```

### Tool with Validation

```typescript
import { z } from "zod";

const FlightSearchSchema = z.object({
  origin: z.string().length(3, "Airport code must be 3 letters"),
  destination: z.string().length(3, "Airport code must be 3 letters"),
  date: z.string().regex(/^\d{4}-\d{2}-\d{2}$/, "Invalid date format"),
  maxStops: z.number().min(0).max(3).optional()
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "search_flights") {
    try {
      const params = FlightSearchSchema.parse(request.params.arguments);
      // Use validated params
      const results = await searchFlights(params);
      return {
        content: [{ type: "text", text: JSON.stringify(results) }]
      };
    } catch (error) {
      if (error instanceof z.ZodError) {
        return {
          content: [
            {
              type: "text",
              text: `Validation error: ${error.errors.map(e => e.message).join(", ")}`
            }
          ],
          isError: true
        };
      }
      throw error;
    }
  }
});
```

## Java Implementation

### Using @Tool Annotation

```java
import org.springframework.ai.tool.Tool;
import org.springframework.ai.tool.ToolParam;
import org.springframework.stereotype.Service;

@Service
public class FlightService {

    @Tool(description = "Search for available flights")
    public String searchFlights(
        @ToolParam(description = "Departure city code (e.g., SFO)") String origin,
        @ToolParam(description = "Arrival city code (e.g., LAX)") String destination,
        @ToolParam(description = "Travel date (YYYY-MM-DD)") String date
    ) {
        // Validate inputs
        if (!isValidAirportCode(origin) || !isValidAirportCode(destination)) {
            return "Invalid airport code format";
        }

        // Search logic
        List<Flight> flights = flightApi.search(origin, destination, date);

        // Format results
        return formatFlightResults(flights);
    }

    @Tool(description = "Book a specific flight")
    public String bookFlight(
        @ToolParam(description = "Flight ID to book") String flightId,
        @ToolParam(description = "Passenger name") String passengerName
    ) {
        try {
            BookingResult result = flightApi.book(flightId, passengerName);
            return String.format(
                "Flight %s booked for %s. Confirmation: %s",
                flightId, passengerName, result.getConfirmationNumber()
            );
        } catch (BookingException e) {
            return "Booking failed: " + e.getMessage();
        }
    }

    private boolean isValidAirportCode(String code) {
        return code != null && code.matches("[A-Z]{3}");
    }
}
```

## JSON Schema Patterns

### Simple Parameters

```json
{
  "type": "object",
  "properties": {
    "query": {
      "type": "string",
      "description": "Search query"
    },
    "limit": {
      "type": "integer",
      "description": "Maximum results",
      "minimum": 1,
      "maximum": 100,
      "default": 10
    }
  },
  "required": ["query"]
}
```

### Enum Parameters

```json
{
  "type": "object",
  "properties": {
    "class": {
      "type": "string",
      "enum": ["economy", "premium", "business", "first"],
      "description": "Cabin class preference"
    },
    "status": {
      "type": "string",
      "enum": ["confirmed", "pending", "cancelled"],
      "description": "Booking status"
    }
  }
}
```

### Nested Objects

```json
{
  "type": "object",
  "properties": {
    "passenger": {
      "type": "object",
      "properties": {
        "firstName": { "type": "string" },
        "lastName": { "type": "string" },
        "dateOfBirth": { "type": "string", "format": "date" }
      },
      "required": ["firstName", "lastName"]
    },
    "contactInfo": {
      "type": "object",
      "properties": {
        "email": { "type": "string", "format": "email" },
        "phone": { "type": "string" }
      }
    }
  },
  "required": ["passenger"]
}
```

### Arrays

```json
{
  "type": "object",
  "properties": {
    "passengers": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": { "type": "string" },
          "age": { "type": "integer" }
        }
      },
      "minItems": 1,
      "maxItems": 9
    },
    "preferredAirlines": {
      "type": "array",
      "items": { "type": "string" },
      "uniqueItems": true
    }
  }
}
```

## Best Practices

### 1. Clear Naming

Use descriptive, action-oriented names:

✅ Good:
- `search_flights`
- `book_hotel`
- `send_email`
- `calculate_tax`

❌ Bad:
- `flight`
- `hotel_thing`
- `email`
- `calc`

### 2. Comprehensive Descriptions

Include what the tool does, when to use it, and any limitations:

```python
@mcp.tool()
async def search_flights(origin: str, destination: str) -> str:
    """Search for available flights between two cities.

    Use this tool when users want to find flights. Returns up to
    10 flight options sorted by price. Only searches US domestic
    flights. For international flights, use search_international_flights.

    Args:
        origin: Three-letter airport code (e.g., SFO, LAX)
        destination: Three-letter airport code
    """
```

### 3. Input Validation

Always validate inputs before processing:

```python
@mcp.tool()
async def search_flights(origin: str, destination: str, date: str) -> str:
    """Search for flights."""
    # Validate airport codes
    if not (len(origin) == 3 and origin.isalpha()):
        return "Invalid origin airport code. Must be 3 letters."

    if not (len(destination) == 3 and destination.isalpha()):
        return "Invalid destination airport code. Must be 3 letters."

    # Validate date format
    try:
        from datetime import datetime
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return "Invalid date format. Use YYYY-MM-DD."

    # Proceed with search
    return await perform_search(origin, destination, date)
```

### 4. Error Messages

Return helpful error messages:

```python
try:
    result = await api_call()
    return format_result(result)
except AuthenticationError:
    return "Authentication failed. Please check API credentials."
except RateLimitError:
    return "Rate limit exceeded. Please try again in a few minutes."
except NetworkError as e:
    return f"Network error: Unable to reach service. {str(e)}"
except Exception as e:
    return f"Unexpected error occurred. Please try again or contact support."
```

### 5. Consistent Return Format

Return structured, parseable text:

```python
@mcp.tool()
async def search_flights(origin: str, destination: str) -> str:
    """Search for flights."""
    flights = await perform_search(origin, destination)

    if not flights:
        return "No flights found for this route."

    # Consistent formatting
    results = []
    for flight in flights:
        results.append(f"""
Flight {flight.number}:
  Departure: {flight.departure_time}
  Arrival: {flight.arrival_time}
  Duration: {flight.duration}
  Price: ${flight.price}
  Stops: {flight.stops}
""".strip())

    return "\n---\n".join(results)
```

### 6. Async Operations

Use async for I/O operations:

```python
import httpx

@mcp.tool()
async def search_flights(origin: str, destination: str) -> str:
    """Search flights."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.example.com/flights",
            params={"origin": origin, "destination": destination}
        )
        data = response.json()
        return format_flights(data)
```

### 7. Tool Composition

Break complex operations into smaller tools:

```python
@mcp.tool()
async def search_flights(origin: str, destination: str, date: str) -> str:
    """Search for flights (read-only)."""
    return await perform_search(origin, destination, date)

@mcp.tool()
async def compare_flight_prices(flight_ids: list[str]) -> str:
    """Compare prices of specific flights."""
    return await compare_prices(flight_ids)

@mcp.tool()
async def book_flight(flight_id: str, passenger_name: str) -> str:
    """Book a specific flight (requires confirmation)."""
    return await book_flight_internal(flight_id, passenger_name)
```

## User Consent Patterns

For sensitive operations, return clear descriptions:

```python
@mcp.tool()
async def send_email(to: str, subject: str, body: str) -> str:
    """Send an email message.

    This will send an actual email from your configured account.
    """
    # Claude will ask for user approval before executing
    result = await email_service.send(to, subject, body)
    return f"Email sent to {to}: {subject}"

@mcp.tool()
async def delete_file(file_path: str) -> str:
    """Delete a file permanently.

    WARNING: This action cannot be undone.
    """
    # Destructive action - user will be prompted
    os.remove(file_path)
    return f"Deleted {file_path}"
```

## Testing Tools

Test tools independently before integration:

```python
# test_tools.py
import asyncio
from server import search_flights

async def test_search():
    result = await search_flights("SFO", "LAX", "2024-03-15")
    print(result)
    assert "Flight" in result

asyncio.run(test_search())
```

## Troubleshooting

### Tool Not Appearing

- Check tool is properly registered
- Verify JSON schema is valid
- Ensure server is running and connected

### Tool Fails to Execute

- Review input validation
- Check for exceptions in logs
- Test tool function independently

### Wrong Parameters Passed

- Verify JSON schema matches expected inputs
- Check parameter types (string vs number)
- Ensure required fields are marked

## Next Steps

See other reference files for:
- **resources.md**: Exposing data sources
- **prompts.md**: Creating prompt templates
- **configuration.md**: Advanced configuration
