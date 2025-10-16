# MetaAgent Quick Start Guide

## What is MetaAgent?

MetaAgent is your AI-powered agent generator - it creates custom sub-agents for you without writing code. Just describe what you need, and MetaAgent builds it.

Think of it as "GitHub Copilot for agents" - you specify requirements, and it generates the complete agent implementation.

## Quick Usage Examples

### 1. Simple Natural Language Request

**You say:**
```
"Create an agent that can check stock prices"
```

**What happens:**
- AI understands your request
- Calls MetaAgent with appropriate parameters
- Generates StockPriceChecker agent
- Saves to Azure Storage
- Confirms completion

**Result:** New agent ready to use after function restart

---

### 2. More Specific Request

**You say:**
```
"I need an agent that sends SMS messages. It should take a phone number and message text as required, and optionally accept a sender ID"
```

**MetaAgent generates:**
- Agent name: SMSMessenger
- Parameters: phone_number (required), message (required), sender_id (optional)
- Proper metadata for OpenAI function calling
- Error handling and JSON responses
- Template code ready for customization

---

### 3. Complex Business Logic

**You say:**
```
"Create an expense report agent that:
- Takes an array of expenses with date, amount, and category
- Calculates totals by category
- Identifies expenses over $500
- Generates a detailed summary report"
```

**MetaAgent provides:**
- Full agent structure with all parameters
- Proper array/object handling
- Template for business logic implementation
- Ready for your specific calculation code

---

## Tips for Best Results

1. **Be Specific**: The more details you provide, the better the generated agent
2. **Describe Parameters**: Mention what inputs the agent needs
3. **Explain Logic**: Describe what the agent should do with the inputs
4. **Mention Dependencies**: If it needs specific libraries, say so

## After Generation

1. Agent is saved to Azure File Storage (multi_agents folder)
2. Restart the function app to load the new agent
3. Customize the generated code if needed
4. Test the agent in conversation
5. Share with your team

## Learn More

- [Full MetaAgent Guide](MetaAgent_Guide.md) - Comprehensive documentation
- [Examples](examples/meta_agent_examples.py) - Practical code examples
- [README](../README.md) - Project overview
