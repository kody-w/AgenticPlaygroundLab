# MetaAgent - Dynamic Sub-Agent Generation

## Overview

The MetaAgent is a powerful tool that allows you to dynamically generate and save custom sub-agents based on your specific needs at runtime. This agent acts as a "GitHub Copilot for agents" - you describe what you need, and it creates the agent for you.

## Features

- **Dynamic Agent Creation**: Generate new agents on-the-fly based on natural language descriptions
- **Automatic Code Generation**: Creates valid Python agent code following the BasicAgent pattern
- **Azure Storage Integration**: Automatically saves generated agents to Azure File Storage
- **Immediate Availability**: Generated agents are loaded on next function restart
- **Parameter Validation**: Validates generated code for syntax and structure
- **Flexible Configuration**: Supports complex parameter schemas and custom imports

## How It Works

The MetaAgent generates complete Python agent code including:
1. Proper class structure inheriting from BasicAgent
2. OpenAI function metadata for integration
3. Parameter handling and validation
4. Error handling and JSON response formatting
5. Documentation and timestamps

Generated agents are saved to the `multi_agents` folder in Azure File Storage and are automatically loaded by the function app on next startup.

## Usage Examples

### Example 1: Simple Greeting Agent

**Request:**
```
"Create an agent called WeatherFetcher that takes a city name and returns weather information for that city"
```

**What the MetaAgent needs:**
- **agent_name**: "WeatherFetcher"
- **agent_description**: "Fetches and returns weather information for a specified city"
- **parameters**: 
  ```json
  {
    "city": {
      "type": "string",
      "description": "Name of the city to get weather for",
      "required": true
    },
    "units": {
      "type": "string",
      "description": "Temperature units (celsius or fahrenheit)",
      "enum": ["celsius", "fahrenheit"],
      "required": false
    }
  }
  ```
- **implementation_logic**: "Fetch weather data for the given city using a weather API and return temperature, conditions, and forecast"

### Example 2: Data Processing Agent

**Request:**
```
"I need an agent that can analyze sales data - it should take an array of sales records and calculate totals, averages, and trends"
```

**What the MetaAgent needs:**
- **agent_name**: "SalesAnalyzer"
- **agent_description**: "Analyzes sales data and provides statistical insights"
- **parameters**:
  ```json
  {
    "sales_data": {
      "type": "array",
      "description": "Array of sales records with amount and date",
      "required": true
    },
    "analysis_type": {
      "type": "string",
      "description": "Type of analysis to perform",
      "enum": ["summary", "trends", "forecasting"],
      "required": true
    },
    "time_period": {
      "type": "string",
      "description": "Time period for analysis (daily, weekly, monthly)",
      "required": false
    }
  }
  ```
- **implementation_logic**: "Calculate total sales, average transaction value, identify trends over time, and provide insights about sales performance"
- **required_imports**: ["import statistics", "from datetime import datetime, timedelta"]

### Example 3: Document Processing Agent

**Request:**
```
"Create an agent that extracts key information from text documents like contracts or invoices"
```

**What the MetaAgent needs:**
- **agent_name**: "DocumentExtractor"
- **agent_description**: "Extracts structured information from unstructured text documents"
- **parameters**:
  ```json
  {
    "document_text": {
      "type": "string",
      "description": "The full text of the document to analyze",
      "required": true
    },
    "extraction_fields": {
      "type": "array",
      "items": {"type": "string"},
      "description": "List of fields to extract (e.g., date, amount, parties)",
      "required": true
    },
    "document_type": {
      "type": "string",
      "description": "Type of document being processed",
      "enum": ["contract", "invoice", "report", "email"],
      "required": false
    }
  }
  ```
- **implementation_logic**: "Use pattern matching and natural language processing to identify and extract specific fields from the document text. Return structured data with extracted values."
- **required_imports**: ["import re", "from typing import List, Dict"]

## Using MetaAgent in Conversation

### Natural Language Approach

You can simply tell the assistant what you need:

```
"I need an agent that can send Slack messages. It should take a channel name, message text, and optionally attachments."
```

The assistant will use MetaAgent to:
1. Parse your requirements
2. Design appropriate parameters
3. Generate the agent code
4. Save it to Azure Storage
5. Inform you about the new agent

### Explicit Approach

For more control, you can specify all parameters:

```
"Use MetaAgent to create:
- Agent name: SlackMessenger
- Description: Sends messages to Slack channels via webhook
- Parameters:
  - channel (string, required): Slack channel name
  - message (string, required): Message to send
  - attachments (array, optional): File attachments
- Logic: Post message to Slack webhook URL with proper formatting
- Imports: import requests, import json"
```

## Parameter Schema Format

The `parameters` field accepts a flexible schema format:

```json
{
  "parameter_name": {
    "type": "string|integer|boolean|array|object",
    "description": "What this parameter is for",
    "required": true|false,
    "enum": ["option1", "option2"],  // Optional: for restricted values
    "items": {"type": "string"},      // For array types
    "properties": {...}               // For object types
  }
}
```

### Supported Types
- **string**: Text values
- **integer**: Numeric values
- **boolean**: true/false values
- **array**: Lists of items
- **object**: Complex nested objects

## Best Practices

### 1. Clear Agent Names
- Use CamelCase (e.g., `DataProcessor`, `EmailSender`)
- Make names descriptive and specific
- Avoid generic names like `Agent1` or `Helper`

### 2. Detailed Descriptions
- Explain what the agent does
- Specify when it should be used
- Include any limitations or requirements

### 3. Well-Defined Parameters
- Mark required parameters appropriately
- Provide clear descriptions for each parameter
- Use enums for restricted value sets
- Set appropriate default values

### 4. Implementation Logic
- Be specific about what the agent should do
- Include any algorithms or methods to use
- Mention external APIs or services if needed
- Describe expected output format

### 5. Required Imports
- List all necessary Python imports
- Include third-party libraries if needed
- Ensure imports match the implementation logic

## Generated Agent Structure

Each generated agent follows this structure:

```python
"""
Auto-generated agent: AgentName
Description: What the agent does
Generated: 2025-01-15 10:30:00
"""

from agents.basic_agent import BasicAgent
import json
# Additional imports...

class AgentName(BasicAgent):
    def __init__(self):
        self.name = 'AgentName'
        self.metadata = {
            "name": self.name,
            "description": "...",
            "parameters": {...}
        }
        super().__init__(name=self.name, metadata=self.metadata)
    
    def perform(self, **kwargs):
        """
        Implementation logic: ...
        """
        # Parameter extraction
        param1 = kwargs.get('param1', default_value)
        
        try:
            # TODO: Implement actual logic
            result = {
                "status": "success",
                "message": "...",
                "data": {...}
            }
            return json.dumps(result)
            
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": f"Error: {str(e)}"
            })
```

## Post-Generation Steps

After MetaAgent creates an agent:

1. **Review the Generated Code**: The agent returns a preview of the generated code
2. **Customize if Needed**: You can download and edit the agent from Azure File Storage
3. **Restart Function**: Generated agents are loaded on next function restart
4. **Test the Agent**: Use the new agent in conversation to verify it works

## Customizing Generated Agents

Generated agents serve as templates. You can enhance them by:

1. **Adding Real API Calls**: Replace placeholder logic with actual API integrations
2. **Implementing Algorithms**: Add specific business logic and calculations
3. **Error Handling**: Enhance error handling for production use
4. **Adding Validation**: Include input validation and sanitization
5. **Logging**: Add detailed logging for debugging

## Limitations and Considerations

### Current Limitations
- Generated agents are templates requiring implementation of actual logic
- No automatic API key management
- Generated code must be reviewed for security before production use
- Agents are not immediately available (requires function restart)

### Security Considerations
- **Review Generated Code**: Always review code before deploying to production
- **Input Validation**: Ensure generated agents validate all inputs
- **API Keys**: Don't include API keys in generated agent code
- **Error Messages**: Avoid exposing sensitive information in error messages

### Performance Considerations
- Large numbers of agents may increase function startup time
- Complex agents should use async operations where appropriate
- Consider caching for agents that make external API calls

## Troubleshooting

### Agent Not Loading
- **Issue**: Generated agent doesn't appear after creation
- **Solution**: Restart the Azure Function App to load new agents

### Syntax Errors
- **Issue**: Generated code has syntax errors
- **Solution**: Review and fix the code in Azure File Storage, or regenerate with corrected parameters

### Import Errors
- **Issue**: Generated agent fails due to missing imports
- **Solution**: Add missing imports to `required_imports` parameter or manually update the agent code

### Runtime Errors
- **Issue**: Agent executes but returns errors
- **Solution**: Implement the actual logic in the perform() method (generated code is a template)

## Examples of Agents You Can Create

### Business Intelligence
- Sales report generator
- KPI calculator
- Trend analyzer
- Forecast generator

### Data Processing
- CSV parser and analyzer
- JSON transformer
- Data validator
- Data aggregator

### Integration
- CRM connector (Salesforce, HubSpot)
- Email sender (SendGrid, SMTP)
- Slack/Teams messenger
- Database query executor

### Utilities
- File format converter
- Text analyzer
- Code formatter
- Regex pattern matcher

### Workflow
- Task creator
- Notification sender
- Status checker
- Report scheduler

## Advanced Usage

### Chaining Agents
Generated agents can call other agents by accessing `self.known_agents` from the Assistant instance.

### Async Operations
For long-running operations, consider using async/await patterns in the generated agent.

### State Management
Agents can use Azure File Storage for persistent state across invocations.

## Getting Help

If you encounter issues or need assistance:

1. Review the generated code preview in the MetaAgent response
2. Check Azure Function logs for error messages
3. Verify all required imports are installed in `requirements.txt`
4. Test with simple parameters first, then increase complexity

## Future Enhancements

Planned improvements for MetaAgent:

- [ ] Real-time agent loading without restart
- [ ] Agent versioning and rollback
- [ ] Automatic dependency detection and installation
- [ ] Agent performance testing and optimization
- [ ] Web-based agent editor
- [ ] Agent marketplace for sharing

---

**Remember**: The MetaAgent is a code generator and template creator. Generated agents provide the structure and framework, but you may need to implement the actual business logic for production use cases.
