# MCP Server - Prompts Reference

## What Are Prompts?

**Prompts** are reusable templates that guide model interactions. They're user-controlled (require explicit invocation) and can reference available resources and tools.

### Protocol Operations

```
prompts/list → Discover available prompts
prompts/get  → Retrieve prompt details with arguments
```

## Prompt Structure

Every prompt consists of:

1. **Name**: Unique identifier (e.g., `plan-vacation`)
2. **Description**: What the prompt does
3. **Arguments**: Optional parameters (with types and defaults)
4. **Messages**: Template content with argument placeholders

## Python Implementation

### Basic Prompt

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-server")

@mcp.prompt()
def code_review_prompt() -> str:
    """Perform a thorough code review."""
    return """Please review the code and provide feedback on:

1. Code quality and readability
2. Potential bugs or errors
3. Performance optimizations
4. Security considerations
5. Best practices adherence

Focus on actionable improvements."""
```

### Prompt with Arguments

```python
@mcp.prompt()
def plan_vacation(destination: str, duration: int, budget: float = None) -> str:
    """Plan a vacation itinerary.

    Args:
        destination: City or country to visit
        duration: Number of days for the trip
        budget: Optional budget in USD
    """
    budget_text = f" with a budget of ${budget:,.2f}" if budget else ""

    return f"""Plan a {duration}-day vacation to {destination}{budget_text}.

Include:
1. Day-by-day itinerary
2. Recommended accommodations
3. Must-see attractions and activities
4. Dining recommendations
5. Transportation tips
6. Estimated costs

Consider local culture, weather, and travel logistics."""
```

### Prompt Referencing Resources

```python
@mcp.prompt()
def analyze_codebase(directory: str) -> str:
    """Analyze code quality of a project directory.

    Args:
        directory: Path to project directory
    """
    return f"""Analyze the codebase in {directory}.

Please review:
1. Code organization and structure
2. Code quality metrics
3. Potential improvements
4. Documentation coverage

Use the file:/// resources to read source files."""
```

### Prompt with Tool Suggestions

```python
@mcp.prompt()
def debug_issue(error_message: str, file_path: str) -> str:
    """Help debug an error in code.

    Args:
        error_message: The error message encountered
        file_path: Path to file where error occurred
    """
    return f"""Debug this error:

Error: {error_message}
File: {file_path}

Steps:
1. Read the file using the get_file tool
2. Analyze the error context
3. Identify the root cause
4. Suggest fixes
5. Explain prevention strategies

Use available tools to gather more context if needed."""
```

## TypeScript Implementation

### Basic Prompt

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { ListPromptsRequestSchema, GetPromptRequestSchema } from "@modelcontextprotocol/sdk/types.js";

const server = new Server({ name: "prompt-server", version: "1.0.0" });

// List prompts
server.setRequestHandler(ListPromptsRequestSchema, async () => ({
  prompts: [
    {
      name: "code-review",
      description: "Perform a thorough code review",
      arguments: []
    },
    {
      name: "plan-vacation",
      description: "Plan a vacation itinerary",
      arguments: [
        {
          name: "destination",
          description: "City or country to visit",
          required: true
        },
        {
          name: "duration",
          description: "Number of days",
          required: true
        },
        {
          name: "budget",
          description: "Budget in USD",
          required: false
        }
      ]
    }
  ]
}));

// Get prompt
server.setRequestHandler(GetPromptRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  if (name === "plan-vacation") {
    const destination = args?.destination as string;
    const duration = args?.duration as number;
    const budget = args?.budget as number | undefined;

    const budgetText = budget ? ` with a budget of $${budget.toLocaleString()}` : "";

    return {
      messages: [
        {
          role: "user",
          content: {
            type: "text",
            text: `Plan a ${duration}-day vacation to ${destination}${budgetText}.\n\nInclude:\n1. Day-by-day itinerary\n2. Accommodations\n3. Attractions\n4. Dining\n5. Transportation`
          }
        }
      ]
    };
  }

  throw new Error(`Unknown prompt: ${name}`);
});
```

## Prompt Patterns

### 1. Analysis Prompts

```python
@mcp.prompt()
def analyze_data(dataset: str, focus: str = "trends") -> str:
    """Analyze a dataset.

    Args:
        dataset: Name of the dataset to analyze
        focus: Analysis focus (trends, anomalies, patterns)
    """
    return f"""Analyze the {dataset} dataset focusing on {focus}.

Steps:
1. Load the dataset using resources
2. Calculate key statistics
3. Identify {focus}
4. Visualize findings
5. Provide actionable insights"""
```

### 2. Generation Prompts

```python
@mcp.prompt()
def generate_api_docs(endpoint: str, method: str) -> str:
    """Generate API documentation.

    Args:
        endpoint: API endpoint path (e.g., /api/users)
        method: HTTP method (GET, POST, PUT, DELETE)
    """
    return f"""Generate comprehensive API documentation for:

Endpoint: {endpoint}
Method: {method}

Include:
1. Description
2. Request parameters
3. Request body schema (if applicable)
4. Response format
5. Status codes
6. Example requests/responses
7. Error handling"""
```

### 3. Workflow Prompts

```python
@mcp.prompt()
def deploy_application(environment: str, version: str) -> str:
    """Guide through application deployment.

    Args:
        environment: Target environment (dev, staging, prod)
        version: Application version to deploy
    """
    return f"""Deploy application version {version} to {environment}.

Checklist:
1. Run tests using run_tests tool
2. Build application
3. Verify configuration
4. Deploy to {environment}
5. Run smoke tests
6. Monitor deployment
7. Rollback procedure if needed

Use available tools to execute each step."""
```

### 4. Interactive Prompts

```python
@mcp.prompt()
def brainstorm_features(product: str, target_audience: str) -> str:
    """Brainstorm product features.

    Args:
        product: Product name or description
        target_audience: Primary user demographic
    """
    return f"""Brainstorm innovative features for {product} targeting {target_audience}.

Consider:
1. User pain points and needs
2. Competitive analysis
3. Technical feasibility
4. Market trends
5. Differentiation opportunities

For each feature idea:
- Description
- User benefit
- Implementation complexity
- Priority (high/medium/low)"""
```

## Multi-Message Prompts

Create conversational templates:

```python
from mcp.types import PromptMessage

@mcp.prompt()
def technical_interview(role: str, experience: str) -> list[PromptMessage]:
    """Conduct a technical interview.

    Args:
        role: Job role (e.g., Senior Backend Engineer)
        experience: Years of experience
    """
    return [
        PromptMessage(
            role="user",
            content=f"I'm interviewing for {role} with {experience} years experience."
        ),
        PromptMessage(
            role="assistant",
            content="I'll conduct a technical interview. Let's start with some warm-up questions."
        ),
        PromptMessage(
            role="user",
            content="Please ask me technical questions appropriate for this role and experience level."
        )
    ]
```

## Dynamic Prompt Content

Generate prompts based on context:

```python
@mcp.prompt()
async def code_review_with_context(file_path: str) -> str:
    """Review code with file context.

    Args:
        file_path: Path to file to review
    """
    # Read file content
    with open(file_path, "r") as f:
        code = f.read()

    # Detect language
    language = detect_language(file_path)

    # Get style guide
    style_guide = get_style_guide(language)

    return f"""Review this {language} code:

```{language}
{code}
```

Check against {language} best practices:
{style_guide}

Provide specific, actionable feedback."""
```

## Best Practices

### 1. Clear Names

Use descriptive, action-oriented names:

✅ Good:
- `plan-vacation`
- `analyze-codebase`
- `debug-error`
- `generate-tests`

❌ Bad:
- `vacation`
- `analyze`
- `bug`
- `tests`

### 2. Comprehensive Descriptions

Explain when and how to use the prompt:

```python
@mcp.prompt()
def refactor_code(file_path: str, goal: str) -> str:
    """Refactor code to improve quality and maintainability.

    Use this prompt when code works but needs improvement in
    structure, readability, or performance. Not for bug fixes
    (use debug-error prompt instead).

    Args:
        file_path: Path to file needing refactoring
        goal: Refactoring objective (readability, performance, testability)
    """
```

### 3. Structured Templates

Provide clear structure and steps:

```python
@mcp.prompt()
def security_audit(component: str) -> str:
    """Audit component for security vulnerabilities."""
    return f"""Perform security audit on {component}.

## Authentication & Authorization
- [ ] Check authentication mechanisms
- [ ] Verify authorization logic
- [ ] Review session management

## Input Validation
- [ ] Validate all user inputs
- [ ] Check for injection vulnerabilities
- [ ] Review file upload handling

## Data Protection
- [ ] Verify encryption at rest
- [ ] Check encryption in transit
- [ ] Review sensitive data handling

## Dependencies
- [ ] Audit third-party libraries
- [ ] Check for known vulnerabilities
- [ ] Review dependency versions

Report findings with severity levels and remediation steps."""
```

### 4. Helpful Defaults

Provide sensible default values:

```python
@mcp.prompt()
def write_blog_post(
    topic: str,
    length: int = 1000,
    tone: str = "professional",
    audience: str = "general"
) -> str:
    """Write a blog post.

    Args:
        topic: Blog post topic
        length: Target word count (default: 1000)
        tone: Writing tone (default: professional)
        audience: Target audience (default: general)
    """
```

### 5. Tool Integration

Reference available tools:

```python
@mcp.prompt()
def investigate_bug(bug_id: str) -> str:
    """Investigate and fix a bug.

    Args:
        bug_id: Bug tracking system ID
    """
    return f"""Investigate bug {bug_id}.

Process:
1. Use get_bug_details tool to fetch bug report
2. Use search_code tool to find relevant code
3. Use get_file tool to read affected files
4. Analyze root cause
5. Propose fix
6. Use run_tests tool to verify fix

Document findings and solution."""
```

## UI Integration

Prompts appear in Claude interfaces:

### Slash Commands
```
/plan-vacation destination="Paris" duration=7
/code-review
/debug-error file="main.py" error="TypeError"
```

### Command Palette
Users can search and select prompts with autocomplete for arguments.

### Context Menus
Right-click menus suggest relevant prompts based on context.

## Testing Prompts

Test prompt generation:

```python
# test_prompts.py
from server import plan_vacation, code_review_prompt

def test_prompts():
    # Test basic prompt
    review = code_review_prompt()
    assert "code quality" in review.lower()

    # Test parameterized prompt
    vacation = plan_vacation("Paris", 7, 5000.0)
    assert "Paris" in vacation
    assert "7-day" in vacation
    assert "$5,000" in vacation

test_prompts()
```

## Prompt Composition

Combine multiple prompts:

```python
@mcp.prompt()
def complete_feature(feature_name: str) -> str:
    """Complete full feature development cycle.

    Args:
        feature_name: Name of feature to implement
    """
    return f"""Implement {feature_name} feature.

Workflow:
1. Design: Use design-feature prompt
2. Implement: Write code
3. Test: Use generate-tests prompt
4. Review: Use code-review prompt
5. Document: Use generate-docs prompt
6. Deploy: Use deploy-application prompt

Execute each step systematically."""
```

## Next Steps

See other reference files for:
- **tools.md**: Implementing executable tools
- **resources.md**: Exposing data sources
- **configuration.md**: Claude Desktop setup and troubleshooting
