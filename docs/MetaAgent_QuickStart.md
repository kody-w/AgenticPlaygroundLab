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
"I need an agent that sends SMS messages. It should take a phone number, message text, and optionally a sender ID"
```

**What MetaAgent generates:**
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
- Generates a summary report"
```

**MetaAgent provides:**
- Full agent structure with all parameters
- Proper array/object handling
- Template for business logic implementation
- Ready for your specific calculation code

---

## Usage in Conversation

### Method 1: Direct Request (Recommended)
Just ask naturally:

```
User: "Make me an agent that can convert currencies"