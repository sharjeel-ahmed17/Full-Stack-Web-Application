# MCP Server - Implementation Guide

This reference provides detailed server implementation patterns for all supported languages.

## Table of Contents

1. [Python (FastMCP)](#python-fastmcp)
2. [TypeScript](#typescript)
3. [Java (Spring AI)](#java-spring-ai)
4. [Kotlin](#kotlin)
5. [C#](#c-net)
6. [Rust](#rust)

---

## Python (FastMCP)

### Setup

```bash
# Install uv package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create project
uv init weather
cd weather
uv venv
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows

# Install dependencies
uv add "mcp[cli]" httpx
```

### Project Structure

```
weather/
├── server.py          # Main server file
├── pyproject.toml     # Dependencies
└── README.md
```

### Complete Server Example

```python
from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
import logging

# Configure logging (writes to stderr, not stdout)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize server
mcp = FastMCP("weather")

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"HTTP error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return None

def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature.get("properties", {})
    return f"""
Event: {props.get("event", "Unknown")}
Area: {props.get("areaDesc", "Unknown")}
Severity: {props.get("severity", "Unknown")}
Description: {props.get("description", "No description available")}
Instructions: {props.get("instruction", "No specific instructions provided")}
""".strip()

@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    state = state.upper()
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    features = data["features"]
    if not features:
        return f"No active alerts for {state}."

    alerts = [format_alert(feature) for feature in features]
    return f"Active alerts for {state}:\n\n" + "\n---\n".join(alerts)

@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    # Get grid point data
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "Unable to fetch forecast data for this location."

    # Get forecast from grid point
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "Unable to fetch forecast details."

    periods = forecast_data["properties"]["periods"][:5]
    forecasts = []

    for period in periods:
        forecast = f"""
{period["name"]}:
Temperature: {period["temperature"]}°{period["temperatureUnit"]}
Wind: {period["windSpeed"]} {period["windDirection"]}
Forecast: {period["detailedForecast"]}
""".strip()
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)

def main():
    """Run the MCP server."""
    logger.info("Starting Weather MCP Server")
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
```

### Running Locally

```bash
uv run server.py
```

### Claude Desktop Configuration

```json
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/you/weather",
        "run",
        "server.py"
      ]
    }
  }
}
```

---

## TypeScript

### Setup

```bash
mkdir weather
cd weather
npm init -y
npm install @modelcontextprotocol/sdk zod
npm install -D @types/node typescript
mkdir src
```

### package.json

```json
{
  "name": "weather",
  "version": "1.0.0",
  "type": "module",
  "bin": {
    "weather": "./build/index.js"
  },
  "scripts": {
    "build": "tsc && chmod +x build/index.js",
    "watch": "tsc --watch",
    "dev": "npm run build && node build/index.js"
  },
  "files": ["build"],
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.0.0",
    "zod": "^3.22.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "typescript": "^5.0.0"
  }
}
```

### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "Node16",
    "moduleResolution": "Node16",
    "outDir": "./build",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "build"]
}
```

### src/index.ts

```typescript
#!/usr/bin/env node
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  McpError,
  ErrorCode,
} from "@modelcontextprotocol/sdk/types.js";

const NWS_API_BASE = "https://api.weather.gov";
const USER_AGENT = "weather-app/1.0";

interface AlertFeature {
  properties: {
    event?: string;
    areaDesc?: string;
    severity?: string;
    description?: string;
    instruction?: string;
  };
}

interface AlertsResponse {
  features: AlertFeature[];
}

async function makeNWSRequest<T>(url: string): Promise<T | null> {
  const headers = {
    "User-Agent": USER_AGENT,
    "Accept": "application/geo+json",
  };

  try {
    const response = await fetch(url, { headers });
    if (!response.ok) {
      console.error(`HTTP error! status: ${response.status}`);
      return null;
    }
    return (await response.json()) as T;
  } catch (error) {
    console.error("Error making NWS request:", error);
    return null;
  }
}

function formatAlert(feature: AlertFeature): string {
  const props = feature.properties;
  return `
Event: ${props.event || "Unknown"}
Area: ${props.areaDesc || "Unknown"}
Severity: ${props.severity || "Unknown"}
Description: ${props.description || "No description"}
Instructions: ${props.instruction || "No instructions"}
`.trim();
}

const server = new Server(
  {
    name: "weather",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "get_alerts",
      description: "Get weather alerts for a US state",
      inputSchema: {
        type: "object",
        properties: {
          state: {
            type: "string",
            description: "Two-letter US state code (e.g. CA, NY)",
          },
        },
        required: ["state"],
      },
    },
    {
      name: "get_forecast",
      description: "Get weather forecast for a location",
      inputSchema: {
        type: "object",
        properties: {
          latitude: {
            type: "number",
            description: "Latitude of the location",
          },
          longitude: {
            type: "number",
            description: "Longitude of the location",
          },
        },
        required: ["latitude", "longitude"],
      },
    },
  ],
}));

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  if (name === "get_alerts") {
    const { state } = args as { state: string };
    const stateCode = state.toUpperCase();
    const url = `${NWS_API_BASE}/alerts/active/area/${stateCode}`;
    const data = await makeNWSRequest<AlertsResponse>(url);

    if (!data) {
      return {
        content: [
          { type: "text", text: "Failed to retrieve alerts data" },
        ],
      };
    }

    const features = data.features || [];
    if (features.length === 0) {
      return {
        content: [
          { type: "text", text: `No active alerts for ${stateCode}` },
        ],
      };
    }

    const formattedAlerts = features.map(formatAlert);
    const alertsText = `Active alerts for ${stateCode}:\n\n${formattedAlerts.join("\n---\n")}`;

    return {
      content: [{ type: "text", text: alertsText }],
    };
  }

  if (name === "get_forecast") {
    const { latitude, longitude } = args as {
      latitude: number;
      longitude: number;
    };

    // Implementation similar to Python version
    // ... (omitted for brevity)

    return {
      content: [{ type: "text", text: "Forecast implementation here" }],
    };
  }

  throw new McpError(
    ErrorCode.MethodNotFound,
    `Unknown tool: ${name}`
  );
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Weather MCP Server running on stdio");
}

main().catch((error) => {
  console.error("Fatal error in main():", error);
  process.exit(1);
});
```

### Build and Run

```bash
npm run build
node build/index.js
```

### Claude Configuration

```json
{
  "mcpServers": {
    "weather": {
      "command": "node",
      "args": ["/Users/you/weather/build/index.js"]
    }
  }
}
```

---

## Java (Spring AI)

### Dependencies (pom.xml)

```xml
<dependencies>
    <dependency>
        <groupId>org.springframework.ai</groupId>
        <artifactId>spring-ai-starter-mcp-server</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-web</artifactId>
    </dependency>
</dependencies>
```

### application.properties

```properties
spring.main.banner-mode=off
logging.pattern.console=
```

### WeatherService.java

```java
package com.example.weather;

import org.springframework.ai.tool.Tool;
import org.springframework.ai.tool.ToolParam;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

@Service
public class WeatherService {

    private final RestClient restClient;

    public WeatherService() {
        this.restClient = RestClient.builder()
            .baseUrl("https://api.weather.gov")
            .defaultHeader("Accept", "application/geo+json")
            .defaultHeader("User-Agent", "WeatherApiClient/1.0")
            .build();
    }

    @Tool(description = "Get weather alerts for a US state")
    public String getAlerts(
        @ToolParam(description = "Two-letter US state code (e.g. CA, NY)")
        String state
    ) {
        String url = String.format("/alerts/active/area/%s", state.toUpperCase());
        try {
            // Make request and format response
            // ... implementation
            return "Alerts for " + state;
        } catch (Exception e) {
            return "Error fetching alerts: " + e.getMessage();
        }
    }

    @Tool(description = "Get weather forecast for a location")
    public String getWeatherForecast(
        @ToolParam(description = "Latitude coordinate") double latitude,
        @ToolParam(description = "Longitude coordinate") double longitude
    ) {
        try {
            // Get grid point
            String pointsUrl = String.format("/points/%.4f,%.4f", latitude, longitude);
            // ... implementation
            return "Forecast for location";
        } catch (Exception e) {
            return "Error fetching forecast: " + e.getMessage();
        }
    }
}
```

### McpServerApplication.java

```java
package com.example.weather;

import org.springframework.ai.mcp.server.McpServer;
import org.springframework.ai.tool.ToolCallbackProvider;
import org.springframework.ai.tool.MethodToolCallbackProvider;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class McpServerApplication {

    public static void main(String[] args) {
        SpringApplication.run(McpServerApplication.class, args);
    }

    @Bean
    public ToolCallbackProvider weatherTools(WeatherService weatherService) {
        return MethodToolCallbackProvider.builder()
            .toolObjects(weatherService)
            .build();
    }
}
```

### Build and Run

```bash
./mvnw clean install
java -Dspring.ai.mcp.server.stdio=true -jar target/weather-1.0.0.jar
```

### Claude Configuration

```json
{
  "mcpServers": {
    "weather": {
      "command": "java",
      "args": [
        "-Dspring.ai.mcp.server.stdio=true",
        "-jar",
        "/Users/you/weather/target/weather-1.0.0.jar"
      ]
    }
  }
}
```

---

## Kotlin

### build.gradle.kts

```kotlin
plugins {
    kotlin("jvm") version "1.9.0"
    kotlin("plugin.serialization") version "1.9.0"
    id("com.github.johnrengelman.shadow") version "8.1.1"
    application
}

repositories {
    mavenCentral()
}

val mcpVersion = "0.4.0"
val slf4jVersion = "2.0.9"
val ktorVersion = "3.1.1"

dependencies {
    implementation("io.modelcontextprotocol:kotlin-sdk:$mcpVersion")
    implementation("org.slf4j:slf4j-nop:$slf4jVersion")
    implementation("io.ktor:ktor-client-core:$ktorVersion")
    implementation("io.ktor:ktor-client-cio:$ktorVersion")
    implementation("io.ktor:ktor-client-content-negotiation:$ktorVersion")
    implementation("io.ktor:ktor-serialization-kotlinx-json:$ktorVersion")
}

application {
    mainClass.set("com.example.WeatherKt")
}
```

### Weather.kt

```kotlin
package com.example

import io.ktor.client.*
import io.ktor.client.call.*
import io.ktor.client.request.*
import io.ktor.client.plugins.contentnegotiation.*
import io.ktor.serialization.kotlinx.json.*
import io.modelcontextprotocol.kotlin.sdk.*
import kotlinx.coroutines.*
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.*

@Serializable
data class AlertsResponse(val features: List<AlertFeature>)

@Serializable
data class AlertFeature(val properties: AlertProperties)

@Serializable
data class AlertProperties(
    val event: String? = null,
    val areaDesc: String? = null,
    val severity: String? = null,
    val description: String? = null,
    val instruction: String? = null
)

fun runMcpServer() {
    val server = Server(
        Implementation(
            name = "weather",
            version = "1.0.0"
        ),
        ServerOptions(
            capabilities = ServerCapabilities(
                tools = ServerCapabilities.Tools(listChanged = true)
            )
        )
    )

    val transport = StdioServerTransport(
        System.`in`.asInput(),
        System.out.asSink().buffered()
    )

    val httpClient = HttpClient {
        install(ContentNegotiation) {
            json(Json { ignoreUnknownKeys = true })
        }
        defaultRequest {
            url("https://api.weather.gov")
            headers {
                append("Accept", "application/geo+json")
                append("User-Agent", "WeatherApiClient/1.0")
            }
        }
    }

    // Register get_alerts tool
    server.addTool(
        name = "get_alerts",
        description = "Get weather alerts for a US state",
        inputSchema = Tool.Input(
            properties = buildJsonObject {
                putJsonObject("state") {
                    put("type", "string")
                    put("description", "Two-letter US state code")
                }
            },
            required = listOf("state")
        )
    ) { request ->
        val state = request.arguments["state"]?.jsonPrimitive?.content
        if (state == null) {
            return@addTool CallToolResult(
                content = listOf(TextContent("State parameter is required"))
            )
        }

        try {
            val response = httpClient.get("/alerts/active/area/${state.uppercase()}")
            val data = response.body<AlertsResponse>()

            if (data.features.isEmpty()) {
                return@addTool CallToolResult(
                    content = listOf(TextContent("No active alerts for $state"))
                )
            }

            val alerts = data.features.map { feature ->
                val props = feature.properties
                """
                Event: ${props.event ?: "Unknown"}
                Area: ${props.areaDesc ?: "Unknown"}
                Severity: ${props.severity ?: "Unknown"}
                Description: ${props.description ?: "No description"}
                """.trimIndent()
            }

            CallToolResult(
                content = alerts.map { TextContent(it) }
            )
        } catch (e: Exception) {
            CallToolResult(
                content = listOf(TextContent("Error: ${e.message}"))
            )
        }
    }

    runBlocking {
        server.connect(transport)
        val done = Job()
        server.onClose {
            done.complete()
        }
        done.join()
    }
}

fun main() = runMcpServer()
```

### Build

```bash
./gradlew shadowJar
```

### Claude Configuration

```json
{
  "mcpServers": {
    "weather": {
      "command": "java",
      "args": [
        "-jar",
        "/Users/you/weather/build/libs/weather-all.jar"
      ]
    }
  }
}
```

---

## C# (.NET)

### Setup

```bash
dotnet new console -n Weather
cd Weather
dotnet add package ModelContextProtocol --prerelease
dotnet add package Microsoft.Extensions.Hosting
```

### Program.cs

```csharp
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using ModelContextProtocol;
using System.Net.Http.Headers;

var builder = Host.CreateEmptyApplicationBuilder(settings: null);

builder.Services.AddMcpServer()
    .WithStdioServerTransport()
    .WithToolsFromAssembly();

builder.Services.AddSingleton(_ =>
{
    var client = new HttpClient()
    {
        BaseAddress = new Uri("https://api.weather.gov")
    };
    client.DefaultRequestHeaders.UserAgent.Add(
        new ProductInfoHeaderValue("weather-tool", "1.0")
    );
    client.DefaultRequestHeaders.Accept.Add(
        new MediaTypeWithQualityHeaderValue("application/geo+json")
    );
    return client;
});

var app = builder.Build();
await app.RunAsync();
```

### Tools/WeatherTools.cs

```csharp
using ModelContextProtocol.Server;
using System.ComponentModel;
using System.Text.Json;

namespace Weather.Tools;

[McpServerToolType]
public static class WeatherTools
{
    [McpServerTool]
    [Description("Get weather alerts for a US state code")]
    public static async Task<string> GetAlerts(
        HttpClient client,
        [Description("Two-letter US state code (e.g. CA, NY)")] string state)
    {
        try
        {
            using var response = await client.GetAsync(
                $"/alerts/active/area/{state.ToUpper()}"
            );
            response.EnsureSuccessStatusCode();

            var content = await response.Content.ReadAsStringAsync();
            using var jsonDocument = JsonDocument.Parse(content);
            var features = jsonDocument.RootElement
                .GetProperty("features")
                .EnumerateArray();

            if (!features.Any())
            {
                return $"No active alerts for {state}";
            }

            var alerts = features.Select(alert =>
            {
                var props = alert.GetProperty("properties");
                return $"""
                Event: {props.GetProperty("event").GetString()}
                Area: {props.GetProperty("areaDesc").GetString()}
                Severity: {props.GetProperty("severity").GetString()}
                Description: {props.GetProperty("description").GetString()}
                """;
            });

            return string.Join("\n---\n", alerts);
        }
        catch (Exception ex)
        {
            return $"Error fetching alerts: {ex.Message}";
        }
    }

    [McpServerTool]
    [Description("Get weather forecast for a location")]
    public static async Task<string> GetForecast(
        HttpClient client,
        [Description("Latitude coordinate")] double latitude,
        [Description("Longitude coordinate")] double longitude)
    {
        // Implementation similar to other languages
        return $"Forecast for {latitude},{longitude}";
    }
}
```

### Build and Run

```bash
dotnet build
dotnet run
```

### Claude Configuration

```json
{
  "mcpServers": {
    "weather": {
      "command": "dotnet",
      "args": [
        "run",
        "--project",
        "/Users/you/Weather",
        "--no-build"
      ]
    }
  }
}
```

---

## Rust

### Cargo.toml

```toml
[package]
name = "weather"
version = "0.1.0"
edition = "2021"

[dependencies]
rmcp = { version = "0.3", features = ["server", "macros", "transport-io"] }
tokio = { version = "1.46", features = ["full"] }
reqwest = { version = "0.12", features = ["json"] }
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
anyhow = "1.0"
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter"] }
```

### src/main.rs

```rust
use anyhow::Result;
use rmcp::{
    ServerHandler, ServiceExt,
    handler::server::{router::tool::ToolRouter, tool::Parameters},
    model::*,
    schemars, tool, tool_handler, tool_router,
};
use serde::Deserialize;

const NWS_API_BASE: &str = "https://api.weather.gov";
const USER_AGENT: &str = "weather-app/1.0";

#[derive(Debug, Deserialize)]
struct AlertsResponse {
    features: Vec<AlertFeature>,
}

#[derive(Debug, Deserialize)]
struct AlertFeature {
    properties: AlertProperties,
}

#[derive(Debug, Deserialize)]
struct AlertProperties {
    event: Option<String>,
    #[serde(rename = "areaDesc")]
    area_desc: Option<String>,
    severity: Option<String>,
    description: Option<String>,
    instruction: Option<String>,
}

#[derive(serde::Deserialize, schemars::JsonSchema)]
pub struct AlertRequest {
    state: String,
}

async fn make_nws_request<T: serde::de::DeserializeOwned>(
    url: &str
) -> Result<T> {
    let client = reqwest::Client::new();
    let response = client
        .get(url)
        .header(reqwest::header::USER_AGENT, USER_AGENT)
        .header(reqwest::header::ACCEPT, "application/geo+json")
        .send()
        .await?
        .error_for_status()?;
    Ok(response.json::<T>().await?)
}

fn format_alert(feature: &AlertFeature) -> String {
    let props = &feature.properties;
    format!(
        "Event: {}\nArea: {}\nSeverity: {}\nDescription: {}",
        props.event.as_deref().unwrap_or("Unknown"),
        props.area_desc.as_deref().unwrap_or("Unknown"),
        props.severity.as_deref().unwrap_or("Unknown"),
        props.description.as_deref().unwrap_or("No description")
    )
}

pub struct Weather {
    tool_router: ToolRouter<Weather>,
}

#[tool_router]
impl Weather {
    fn new() -> Self {
        Self {
            tool_router: Self::tool_router(),
        }
    }

    #[tool(description = "Get weather alerts for a US state")]
    async fn get_alerts(
        &self,
        Parameters(AlertRequest { state }): Parameters<AlertRequest>,
    ) -> String {
        let url = format!(
            "{}/alerts/active/area/{}",
            NWS_API_BASE,
            state.to_uppercase()
        );

        match make_nws_request::<AlertsResponse>(&url).await {
            Ok(data) => {
                if data.features.is_empty() {
                    format!("No active alerts for {}", state)
                } else {
                    data.features
                        .iter()
                        .map(format_alert)
                        .collect::<Vec<_>>()
                        .join("\n---\n")
                }
            }
            Err(_) => "Unable to fetch alerts".to_string(),
        }
    }
}

#[tool_handler]
impl ServerHandler for Weather {
    fn get_info(&self) -> ServerInfo {
        ServerInfo {
            capabilities: ServerCapabilities::builder()
                .enable_tools()
                .build(),
            ..Default::default()
        }
    }
}

#[tokio::main]
async fn main() -> Result<()> {
    tracing_subscriber::fmt::init();

    let transport = (tokio::io::stdin(), tokio::io::stdout());
    let service = Weather::new().serve(transport).await?;
    service.waiting().await?;

    Ok(())
}
```

### Build

```bash
cargo build --release
```

### Claude Configuration

```json
{
  "mcpServers": {
    "weather": {
      "command": "/Users/you/weather/target/release/weather"
    }
  }
}
```

---

## Common Patterns Across Languages

### Error Handling

All implementations should:
- Catch and handle HTTP errors gracefully
- Return user-friendly error messages
- Log errors to stderr (never stdout for stdio transport)

### Async Operations

- Python: Use `async/await` with `asyncio`
- TypeScript: Native `async/await`
- Java: Use reactive or blocking approaches
- Kotlin: Use coroutines
- C#: `Task`-based async
- Rust: `async/await` with tokio runtime

### Input Validation

- Define clear JSON schemas for tool inputs
- Validate parameters before processing
- Return descriptive errors for invalid inputs

### Testing

Test servers locally before Claude integration:
```bash
# Run server directly
./your-server

# Send test JSON-RPC message
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | ./your-server
```

## Next Steps

See other reference files for:
- **tools.md**: Implementing tools with schemas
- **resources.md**: Exposing data sources
- **prompts.md**: Creating prompt templates
- **configuration.md**: Advanced config and deployment
