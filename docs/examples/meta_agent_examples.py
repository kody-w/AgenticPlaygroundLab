#!/usr/bin/env python3
"""
Example: Using MetaAgent to create a custom sub-agent

This example demonstrates how to use the MetaAgent to dynamically generate
a custom agent for a specific use case - in this case, a cryptocurrency
price checker agent.
"""

import json
import sys
from unittest.mock import MagicMock, patch

# Mock storage manager for demo purposes
mock_storage = MagicMock()
mock_storage.write_file = MagicMock(return_value=True)

# Patch AzureFileStorageManager before importing MetaAgent
with patch('utils.azure_file_storage.AzureFileStorageManager', return_value=mock_storage):
    from agents.meta_agent import MetaAgent

def create_crypto_price_agent():
    """
    Example: Creating a cryptocurrency price checker agent
    """
    print("=" * 70)
    print("Example: Creating a Cryptocurrency Price Checker Agent")
    print("=" * 70)
    
    # Initialize MetaAgent (in production, this happens automatically)
    with patch('utils.azure_file_storage.AzureFileStorageManager', return_value=mock_storage):
        meta_agent = MetaAgent()
    
    # Define what we want the agent to do
    print("\n📝 Agent Specification:")
    print("  Name: CryptoPriceChecker")
    print("  Purpose: Fetch current cryptocurrency prices")
    print("  Parameters: cryptocurrency symbol and currency")
    
    # Call MetaAgent to generate the agent
    result_json = meta_agent.perform(
        agent_name="CryptoPriceChecker",
        agent_description="Fetches current cryptocurrency prices from a price API and returns price data including current value, 24h change, and market cap",
        parameters={
            "crypto_symbol": {
                "type": "string",
                "description": "Cryptocurrency symbol (e.g., BTC, ETH, DOGE)",
                "required": True
            },
            "currency": {
                "type": "string",
                "description": "Target currency for price (e.g., USD, EUR, GBP)",
                "enum": ["USD", "EUR", "GBP", "JPY"],
                "required": False
            }
        },
        implementation_logic="""
        Connect to a cryptocurrency price API (like CoinGecko or CoinMarketCap).
        Fetch the current price for the specified cryptocurrency in the target currency.
        Return a formatted response with:
        - Current price
        - 24-hour price change (percentage)
        - Market cap
        - Last updated timestamp
        Handle API errors gracefully and return appropriate error messages.
        """,
        required_imports=[
            "import requests",
            "from datetime import datetime"
        ]
    )
    
    result = json.loads(result_json)
    
    # Display results
    print("\n✅ Agent Generation Result:")
    print(f"  Status: {result['status']}")
    
    if result['status'] == 'success':
        print(f"  Agent Name: {result['agent_name']}")
        print(f"  File Name: {result['file_name']}")
        print(f"  Location: {result['location']}")
        print(f"\n📄 Generated Code Preview:")
        print("-" * 70)
        print(result.get('generated_code_preview', 'No preview available'))
        print("-" * 70)
        print(f"\n💡 Note: {result['note']}")
    else:
        print(f"  Error: {result.get('message', 'Unknown error')}")
    
    return result

def create_task_manager_agent():
    """
    Example: Creating a task management agent
    """
    print("\n\n" + "=" * 70)
    print("Example: Creating a Task Manager Agent")
    print("=" * 70)
    
    with patch('utils.azure_file_storage.AzureFileStorageManager', return_value=mock_storage):
        meta_agent = MetaAgent()
    
    print("\n📝 Agent Specification:")
    print("  Name: TaskManager")
    print("  Purpose: Create, update, and track tasks")
    print("  Parameters: action, task details")
    
    result_json = meta_agent.perform(
        agent_name="TaskManager",
        agent_description="Manages tasks including creation, updating status, setting priorities, and retrieving task lists. Integrates with task storage system.",
        parameters={
            "action": {
                "type": "string",
                "description": "Action to perform on tasks",
                "enum": ["create", "update", "list", "complete", "delete"],
                "required": True
            },
            "task_title": {
                "type": "string",
                "description": "Title of the task",
                "required": False
            },
            "task_description": {
                "type": "string",
                "description": "Detailed description of the task",
                "required": False
            },
            "priority": {
                "type": "string",
                "description": "Task priority level",
                "enum": ["low", "medium", "high", "urgent"],
                "required": False
            },
            "due_date": {
                "type": "string",
                "description": "Due date in YYYY-MM-DD format",
                "required": False
            },
            "task_id": {
                "type": "string",
                "description": "Unique task identifier (for update/complete/delete)",
                "required": False
            }
        },
        implementation_logic="""
        Implement a task management system that:
        1. CREATE: Generate unique task ID, store task with all details
        2. UPDATE: Modify existing task properties
        3. LIST: Return all tasks, optionally filtered by status or priority
        4. COMPLETE: Mark task as completed with timestamp
        5. DELETE: Remove task from storage
        
        Store tasks in Azure File Storage for persistence.
        Return formatted task information with clear status indicators.
        Handle edge cases like missing task IDs or invalid dates.
        """,
        required_imports=[
            "import uuid",
            "from datetime import datetime",
            "from utils.azure_file_storage import AzureFileStorageManager"
        ]
    )
    
    result = json.loads(result_json)
    
    print("\n✅ Agent Generation Result:")
    print(f"  Status: {result['status']}")
    if result['status'] == 'success':
        print(f"  Agent Name: {result['agent_name']}")
        print(f"  File Name: {result['file_name']}")
    
    return result

def create_code_reviewer_agent():
    """
    Example: Creating a code review agent
    """
    print("\n\n" + "=" * 70)
    print("Example: Creating a Code Review Agent")
    print("=" * 70)
    
    with patch('utils.azure_file_storage.AzureFileStorageManager', return_value=mock_storage):
        meta_agent = MetaAgent()
    
    print("\n📝 Agent Specification:")
    print("  Name: CodeReviewer")
    print("  Purpose: Review code for quality, security, and best practices")
    print("  Parameters: code content, language, review focus")
    
    result_json = meta_agent.perform(
        agent_name="CodeReviewer",
        agent_description="Reviews code for potential issues including security vulnerabilities, performance problems, code style violations, and adherence to best practices",
        parameters={
            "code": {
                "type": "string",
                "description": "The code to review",
                "required": True
            },
            "language": {
                "type": "string",
                "description": "Programming language of the code",
                "enum": ["python", "javascript", "typescript", "java", "csharp", "go", "rust"],
                "required": True
            },
            "review_focus": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Areas to focus on during review",
                "required": False
            }
        },
        implementation_logic="""
        Analyze the provided code and generate a comprehensive review report:
        1. Security: Check for SQL injection, XSS, hardcoded secrets, etc.
        2. Performance: Identify inefficient algorithms, unnecessary loops
        3. Style: Check formatting, naming conventions, documentation
        4. Best Practices: Language-specific idioms and patterns
        5. Bugs: Potential runtime errors, logic issues
        
        Return a structured report with:
        - Overall score (1-10)
        - List of issues (severity: critical/high/medium/low)
        - Specific line numbers where applicable
        - Suggested fixes for each issue
        - Positive highlights of good practices
        """,
        required_imports=[
            "import re",
            "from typing import List, Dict"
        ]
    )
    
    result = json.loads(result_json)
    
    print("\n✅ Agent Generation Result:")
    print(f"  Status: {result['status']}")
    if result['status'] == 'success':
        print(f"  Agent Name: {result['agent_name']}")
        print(f"  File Name: {result['file_name']}")
    
    return result

def main():
    """Run all examples"""
    print("\n" + "🤖 " * 20)
    print("MetaAgent Usage Examples")
    print("Dynamic Sub-Agent Generation with GitHub Copilot-like Experience")
    print("🤖 " * 20 + "\n")
    
    # Example 1: Cryptocurrency Price Checker
    create_crypto_price_agent()
    
    # Example 2: Task Manager
    create_task_manager_agent()
    
    # Example 3: Code Reviewer
    create_code_reviewer_agent()
    
    print("\n\n" + "=" * 70)
    print("📚 Summary")
    print("=" * 70)
    print("""
These examples demonstrate how MetaAgent can generate specialized agents
for different use cases without writing any code manually.

Key Benefits:
✅ No coding required - just describe what you need
✅ Automatic parameter schema generation
✅ Built-in error handling and validation
✅ Integration with Azure File Storage
✅ Immediate availability after function restart

Next Steps:
1. Customize the generated agents with actual API integrations
2. Add additional error handling for production use
3. Test the agents in real conversations
4. Share useful agents with your team

For more information, see: docs/MetaAgent_Guide.md
    """)

if __name__ == "__main__":
    main()
