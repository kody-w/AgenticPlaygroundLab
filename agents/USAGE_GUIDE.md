# Directory Steward Agent - Usage Guide

This guide provides practical examples and use cases for the Directory Steward Agent.

## Quick Start

The Directory Steward Agent is automatically loaded when you start your Copilot Agent 365 function app. Simply interact with it using natural language.

## Common Use Cases

### 1. Understanding Your Repository Structure

**Scenario**: You're new to the codebase and want to understand its organization.

**Natural Language Request**:
```
"Show me the directory structure of this project"
"Give me an overview of the repository layout"
"What's the file structure look like?"
```

**Direct API Call**:
```json
{
    "action": "analyze_structure",
    "path": "/path/to/repository",
    "depth": 3
}
```

**Expected Output**:
```
📁 Directory Structure Analysis: AgenticPlaygroundLab
==============================================================
├── 📝 CLAUDE.md
├── 📝 README.md
├── 📁 agents/
│   ├── 🐍 basic_agent.py
│   ├── 🐍 context_memory_agent.py
│   ├── 🐍 directory_steward_agent.py
│   └── ...
├── 📁 docs/
│   ├── 📝 AGENT_DEVELOPMENT.md
│   └── ...
└── 🐍 function_app.py
```

---

### 2. Finding Specific Files

**Scenario**: You need to locate all Python files in the project.

**Natural Language Request**:
```
"Find all Python files"
"Search for *.py files"
"Show me all the Python code files"
```

**Direct API Call**:
```json
{
    "action": "search_files",
    "pattern": "*.py"
}
```

**Expected Output**:
```
🔍 Search Results for '*.py' in AgenticPlaygroundLab:
==============================================================
📄 Files (7):
  • agents/basic_agent.py (153.0 B)
  • agents/directory_steward_agent.py (23.7 KB)
  • function_app.py (29.8 KB)
  ...
```

---

### 3. Analyzing Codebase Statistics

**Scenario**: You want to understand the composition of your codebase.

**Natural Language Request**:
```
"Give me statistics about the codebase"
"What file types are in this project?"
"How big is this repository?"
```

**Direct API Call**:
```json
{
    "action": "get_statistics"
}
```

**Expected Output**:
```
📊 Directory Statistics: AgenticPlaygroundLab
==============================================================
📁 Overview:
  • Total files: 30
  • Total size: 1.4 MB

📋 File Types (Top 10):
  • .md: 12 files (40.0%)
  • .py: 7 files (23.3%)
  • .json: 3 files (10.0%)
  ...
```

---

### 4. Finding Code References

**Scenario**: You need to find where a specific class or function is used.

**Natural Language Request**:
```
"Find files that contain 'BasicAgent'"
"Where is BasicAgent mentioned?"
"Search for BasicAgent in the code"
```

**Direct API Call**:
```json
{
    "action": "find_pattern",
    "pattern": "BasicAgent"
}
```

**Expected Output**:
```
🔎 Pattern Search Results for 'BasicAgent':
==============================================================
Found in 13 files:
  • function_app.py (7 occurrences)
  • docs/AGENT_DEVELOPMENT.md (12 occurrences)
  • agents/manage_memory_agent.py (2 occurrences)
  ...
```

---

### 5. Repository Health Check

**Scenario**: You want to ensure the repository is well-maintained.

**Natural Language Request**:
```
"Check the repository health"
"Are there any issues with the codebase?"
"Perform a health check"
```

**Direct API Call**:
```json
{
    "action": "health_check"
}
```

**Expected Output**:
```
🏥 Repository Health Check: AgenticPlaygroundLab
==============================================================
✅ Repository is in good health!

💡 Suggestions:
💡 Consider adding: LICENSE
```

---

### 6. Getting Maintenance Suggestions

**Scenario**: You want to improve the organization and quality of your codebase.

**Natural Language Request**:
```
"What maintenance tasks should I do?"
"Give me suggestions for improving the repository"
"How can I make this codebase better?"
```

**Direct API Call**:
```json
{
    "action": "suggest_maintenance"
}
```

**Expected Output**:
```
🔧 Maintenance Suggestions for AgenticPlaygroundLab
==============================================================
✅ Found 5 agent files in agents/ directory
📚 Documentation: 9 markdown files in docs/
💡 Consider adding tests for better code quality
✅ Configuration files found: requirements.txt
...
```

---

### 7. Exploring Specific Directories

**Scenario**: You want to see what's inside a specific folder.

**Natural Language Request**:
```
"List the contents of the agents directory"
"What's in the agents folder?"
"Show me files in agents/"
```

**Direct API Call**:
```json
{
    "action": "list_directory",
    "path": "/path/to/agents"
}
```

**Expected Output**:
```
📂 Contents of agents:
==============================================================
📄 Files (6):
  • basic_agent.py (153.0 B)
  • context_memory_agent.py (7.3 KB)
  • directory_steward_agent.py (23.7 KB)
  ...
```

---

### 8. Getting File Details

**Scenario**: You need detailed information about a specific file.

**Natural Language Request**:
```
"Tell me about function_app.py"
"Get info on function_app.py"
"What can you tell me about the function_app.py file?"
```

**Direct API Call**:
```json
{
    "action": "get_file_info",
    "path": "/path/to/function_app.py"
}
```

**Expected Output**:
```
📄 File Information: function_app.py
==============================================================
📍 Path: /home/runner/work/.../function_app.py
📏 Size: 29.8 KB
📅 Modified: 2025-01-15 10:30:45
📋 Type: .py
📝 Lines: 485
```

---

## Advanced Usage

### Combining with Other Agents

The Directory Steward Agent works seamlessly with other agents:

**Example**: Finding and documenting files
```
"Find all agent files and tell me what they do"
→ Directory Steward finds the files
→ Context Memory recalls what each agent does
→ Response combines both insights
```

**Example**: Health check and memory storage
```
"Check repository health and remember any issues"
→ Directory Steward performs health check
→ Manage Memory stores findings for future reference
```

### Custom Search Patterns

You can use various search patterns:

- `*.py` - Find all Python files
- `*.md` - Find all Markdown files
- `agent` - Find files with "agent" in the name
- `test*` - Find files starting with "test"
- `*config*` - Find files containing "config"

### Depth Control

Control how deep the agent searches:

```json
{
    "action": "analyze_structure",
    "depth": 1  // Only top-level directory
}
```

```json
{
    "action": "analyze_structure",
    "depth": 5  // Deep traversal (max 10)
}
```

## Integration Examples

### Via Web Chat Interface

1. Open `index.html` in your browser
2. Type your natural language request
3. The agent responds with formatted results

### Via REST API

```bash
curl -X POST http://localhost:7071/api/businessinsightbot_function \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "Show me the directory structure",
    "conversation_history": []
  }'
```

### Via Power Automate (Teams Integration)

1. User sends message in Teams
2. Copilot Studio captures intent
3. Power Automate enriches with context
4. Azure Function executes agent
5. Results display in Teams

### Via Python Script

```python
from agents.directory_steward_agent import DirectoryStewardAgent

# Initialize agent
agent = DirectoryStewardAgent()

# Perform action
result = agent.perform(
    action='analyze_structure',
    path='/path/to/repo',
    depth=2
)

print(result)
```

## Best Practices

### For Effective Queries

1. **Be Specific**: Instead of "find files", say "find all Python files"
2. **Use Context**: "Show me the structure of the agents directory"
3. **Combine Actions**: "Check health and suggest improvements"

### For Performance

1. **Limit Depth**: Use `depth=2` or `depth=3` for large repositories
2. **Narrow Scope**: Specify paths instead of searching entire repository
3. **Use Patterns**: Use specific patterns instead of broad searches

### For Maintenance

1. **Regular Checks**: Run health checks weekly
2. **Track Changes**: Compare statistics over time
3. **Act on Suggestions**: Address maintenance recommendations promptly

## Troubleshooting

### Issue: Agent Not Responding

**Solution**:
1. Verify function app is running: `func start`
2. Check agent loaded: Look for "Loaded agent: DirectorySteward" in logs
3. Restart function app if needed

### Issue: Permission Denied

**Solution**:
1. Check file permissions: `ls -la /path/to/directory`
2. Run with appropriate privileges
3. Verify path is accessible

### Issue: No Results Found

**Solution**:
1. Verify path exists
2. Check search pattern syntax
3. Try broader search terms
4. Check if files are hidden (start with `.`)

### Issue: Slow Performance

**Solution**:
1. Reduce depth parameter
2. Search smaller directory scope
3. Use more specific patterns
4. Exclude large directories

## Examples by Role

### For Developers

```
"Find all test files"
"Show me the code structure"
"Where is the API endpoint defined?"
"Find files containing 'TODO'"
```

### For DevOps Engineers

```
"Check repository health"
"Find all configuration files"
"What's taking up the most space?"
"List all deployment scripts"
```

### For Team Leads

```
"Give me project statistics"
"What's our code-to-docs ratio?"
"Find all incomplete features"
"Check for maintenance needs"
```

### For Documentation Writers

```
"Find all markdown files"
"Where are the docs located?"
"List files that need documentation"
"Find README files"
```

## Tips & Tricks

### Quick Commands

- `"ls agents"` - List agents directory
- `"tree"` - Show directory tree
- `"stats"` - Get statistics
- `"health"` - Run health check

### Alias Natural Language

The agent understands various phrasings:
- "Show me" = "List" = "Display" = "Get"
- "Find" = "Search" = "Locate"
- "Check" = "Analyze" = "Review"

### Power User Tips

1. **Chain Actions**: Ask for multiple things in sequence
2. **Use Memory**: Agent remembers previous queries in conversation
3. **Natural Language**: Don't worry about exact syntax
4. **Explore**: Try different actions to discover capabilities

## Next Steps

1. **Explore**: Try all 8 actions to understand capabilities
2. **Customize**: Modify agent for your specific needs
3. **Integrate**: Connect with other agents for powerful workflows
4. **Share**: Document your use cases and share with team

## Support

- **Documentation**: See `README_DIRECTORY_STEWARD.md` for full details
- **Issues**: Report bugs on GitHub
- **Questions**: Use GitHub Discussions
- **Contributions**: Submit pull requests for improvements

---

**Happy Directory Stewarding! 🚀**
