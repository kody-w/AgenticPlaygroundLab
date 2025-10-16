# Directory Steward Agent

## Overview

The **Directory Steward Agent** is an autonomous AI agent designed to monitor, analyze, and maintain directory structures in the Copilot Agent 365 ecosystem. It provides comprehensive directory stewardship capabilities, helping you understand, organize, and maintain your codebase.

## Features

### 🔍 **Directory Analysis**
- Visualize directory structures with tree-style output
- Count files, directories, and calculate total sizes
- Identify file types and their distributions
- Generate comprehensive directory statistics

### 🔎 **Intelligent Search**
- Search for files by name patterns
- Find files containing specific content
- Pattern matching across multiple file types
- Recursive search with depth control

### 📊 **Repository Health Monitoring**
- Detect large files that might need attention
- Identify missing important files (README, .gitignore, etc.)
- Find empty directories
- Provide health status reports

### 🔧 **Maintenance Suggestions**
- Analyze agent organization
- Check documentation coverage
- Identify test files
- Provide actionable recommendations

### 📁 **File Operations**
- List directory contents
- Get detailed file information
- View file metadata and statistics
- Track file sizes and modification dates

## Usage

The Directory Steward Agent automatically loads with your Copilot Agent 365 deployment and can be invoked through natural language or direct API calls.

### Natural Language Examples

Simply talk to your AI assistant:

- "Show me the directory structure"
- "Find all Python files"
- "What's the health status of the repository?"
- "Search for files containing 'agent'"
- "Give me statistics about the codebase"
- "What maintenance tasks should I do?"
- "List the contents of the agents directory"
- "Tell me about the function_app.py file"

### Direct API Usage

You can also invoke the agent directly through function calls:

```python
# Analyze directory structure
{
    "action": "analyze_structure",
    "path": "/path/to/directory",
    "depth": 3
}

# Search for files
{
    "action": "search_files",
    "path": "/path/to/search",
    "pattern": "*.py"
}

# Get repository statistics
{
    "action": "get_statistics",
    "path": "/path/to/directory"
}

# Find pattern in files
{
    "action": "find_pattern",
    "path": "/path/to/search",
    "pattern": "BasicAgent"
}

# Perform health check
{
    "action": "health_check",
    "path": "/path/to/repository"
}

# List directory contents
{
    "action": "list_directory",
    "path": "/path/to/directory"
}

# Get file information
{
    "action": "get_file_info",
    "path": "/path/to/file.py"
}

# Get maintenance suggestions
{
    "action": "suggest_maintenance",
    "path": "/path/to/repository"
}
```

## Actions

### `analyze_structure`
Generates a visual tree representation of the directory structure.

**Parameters:**
- `path` (optional): Directory path to analyze
- `depth` (optional): Maximum depth for traversal (default: 3)

**Example Output:**
```
📁 Directory Structure Analysis: AgenticPlaygroundLab

==============================================================
📁 AgenticPlaygroundLab/
├── 📁 agents/
│   ├── 🐍 basic_agent.py
│   ├── 🐍 context_memory_agent.py
│   ├── 🐍 directory_steward_agent.py
│   ├── 🐍 email_drafting_agent.py
│   └── 🐍 manage_memory_agent.py
├── 📁 docs/
│   ├── 📝 AGENT_DEVELOPMENT.md
│   └── 📝 ARCHITECTURE.md
├── 🐍 function_app.py
├── 📝 README.md
└── 📋 requirements.txt

==============================================================

📊 Summary:
  • Total directories: 5
  • Total files: 25
  • Total size: 1.2 MB
```

### `search_files`
Search for files matching a specific pattern.

**Parameters:**
- `path` (optional): Directory to search within
- `pattern` (required): Search pattern (e.g., "*.py", "agent", "test")

**Example Output:**
```
🔍 Search Results for '*.py' in AgenticPlaygroundLab:

==============================================================

📄 Files (12):
  • agents/basic_agent.py (512 B)
  • agents/context_memory_agent.py (3.2 KB)
  • agents/directory_steward_agent.py (15.4 KB)
  • function_app.py (12.8 KB)
  ...
```

### `get_statistics`
Generate detailed statistics about the directory.

**Parameters:**
- `path` (optional): Directory to analyze

**Example Output:**
```
📊 Directory Statistics: AgenticPlaygroundLab

==============================================================

📁 Overview:
  • Total files: 42
  • Total size: 2.5 MB

📋 File Types (Top 10):
  • .py: 15 files (35.7%)
  • .md: 10 files (23.8%)
  • .json: 5 files (11.9%)
  • .txt: 3 files (7.1%)
  ...
```

### `find_pattern`
Find files containing specific content.

**Parameters:**
- `path` (optional): Directory to search
- `pattern` (required): Text pattern to find

**Example Output:**
```
🔎 Pattern Search Results for 'BasicAgent':

==============================================================

Found in 8 files:

  • agents/directory_steward_agent.py (3 occurrences)
  • agents/manage_memory_agent.py (2 occurrences)
  • agents/email_drafting_agent.py (2 occurrences)
  • function_app.py (5 occurrences)
  ...
```

### `health_check`
Perform a comprehensive health check on the repository.

**Parameters:**
- `path` (optional): Repository path to check

**Example Output:**
```
🏥 Repository Health Check: AgenticPlaygroundLab

==============================================================

✅ Repository is in good health!

💡 Suggestions:
  • Consider adding automated tests
  • Document API endpoints
  🗑️  Found 2 empty directories that could be cleaned up
```

### `list_directory`
List all contents of a specific directory.

**Parameters:**
- `path` (required): Directory path to list

**Example Output:**
```
📂 Contents of agents:

==============================================================

📄 Files (5):
  • basic_agent.py (512 B)
  • context_memory_agent.py (3.2 KB)
  • directory_steward_agent.py (15.4 KB)
  • email_drafting_agent.py (2.1 KB)
  • manage_memory_agent.py (4.5 KB)
```

### `get_file_info`
Get detailed information about a specific file.

**Parameters:**
- `path` (required): File path

**Example Output:**
```
📄 File Information: function_app.py

==============================================================

📍 Path: /home/runner/work/AgenticPlaygroundLab/AgenticPlaygroundLab/function_app.py
📏 Size: 12.8 KB
📅 Modified: 2025-01-15 10:30:45
📅 Created: 2025-01-10 08:15:20
📋 Type: .py
📝 Lines: 485
```

### `suggest_maintenance`
Get actionable maintenance suggestions.

**Parameters:**
- `path` (optional): Repository path

**Example Output:**
```
🔧 Maintenance Suggestions for AgenticPlaygroundLab

==============================================================

✅ Found 5 agent files in agents/ directory
📚 Documentation: 8 markdown files in docs/
✅ Found 0 test-related files
✅ Configuration files found: requirements.txt, local.settings.json

🎯 General Recommendations:
  • Keep agents in the agents/ directory
  • Document each agent's purpose and usage
  • Regularly review and update dependencies
  • Maintain consistent code style
  • Use version control for all changes
```

## Implementation Details

### Architecture

The Directory Steward Agent follows the standard Copilot Agent 365 architecture:

```python
class DirectoryStewardAgent(BasicAgent):
    def __init__(self):
        self.name = 'DirectorySteward'
        self.metadata = { ... }  # OpenAI function schema
        super().__init__(self.name, self.metadata)
    
    def perform(self, **kwargs) -> str:
        # Execute actions based on parameters
        pass
```

### Key Components

1. **Tree Builder**: Generates visual directory trees with icons
2. **File Scanner**: Recursively scans directories with filtering
3. **Statistics Engine**: Calculates file counts, sizes, and distributions
4. **Pattern Matcher**: Searches files by name and content
5. **Health Analyzer**: Identifies issues and provides recommendations

### Security Features

- **Path Validation**: Ensures all paths are within repository bounds
- **Permission Handling**: Gracefully handles permission errors
- **Ignore Lists**: Automatically skips hidden files and common ignore patterns
- **Safe File Reading**: Uses error handling and encoding fallbacks

### Performance Optimizations

- **Depth Limiting**: Prevents excessive recursion
- **Result Limiting**: Caps output to prevent overwhelming responses
- **Efficient Filtering**: Skips unnecessary directories (node_modules, .venv, etc.)
- **Lazy Loading**: Only reads file contents when needed

## Customization

### Adding New Actions

To add a new action, modify the `directory_steward_agent.py` file:

1. Add the action to the `enum` in metadata:
```python
"action": {
    "type": "string",
    "enum": [
        "analyze_structure",
        "your_new_action",  # Add here
        ...
    ]
}
```

2. Implement the action method:
```python
def _your_new_action(self, path: str, **kwargs) -> str:
    """Your action implementation."""
    # Your code here
    return "Result"
```

3. Add the dispatch in `perform()`:
```python
elif action == 'your_new_action':
    return self._your_new_action(path)
```

### Modifying File Icons

Edit the `_get_file_icon()` method to customize file type icons:

```python
def _get_file_icon(self, filename: str) -> str:
    ext = os.path.splitext(filename)[1].lower()
    icons = {
        '.py': '🐍',
        '.js': '📜',
        '.your_ext': '🎨',  # Add custom icons
        ...
    }
    return icons.get(ext, '📄')
```

### Adjusting Ignore Patterns

Modify the ignore list in various methods:

```python
# Current ignore list
ignored = ['.git', '__pycache__', 'node_modules', '.venv']

# Add more patterns
ignored = ['.git', '__pycache__', 'node_modules', '.venv', 'dist', 'build']
```

## Integration Examples

### Azure Function Call

```json
POST /api/businessinsightbot_function
{
    "user_input": "Analyze the directory structure",
    "conversation_history": []
}
```

### Power Automate Flow

The agent integrates seamlessly with Power Automate:

1. User sends message in Teams
2. Copilot Studio routes to Power Automate
3. Power Automate calls Azure Function
4. DirectorySteward agent executes
5. Results return to user in Teams

### Python Script

```python
from agents.directory_steward_agent import DirectoryStewardAgent

# Create agent instance
agent = DirectoryStewardAgent()

# Analyze structure
result = agent.perform(
    action='analyze_structure',
    path='/path/to/repo',
    depth=2
)

print(result)
```

## Best Practices

### For Users

1. **Be Specific**: Provide clear paths and patterns for better results
2. **Start Simple**: Use basic actions first before complex queries
3. **Review Suggestions**: Always review maintenance suggestions before implementing
4. **Regular Checks**: Run health checks periodically to catch issues early

### For Developers

1. **Error Handling**: Always wrap file operations in try-except blocks
2. **Path Security**: Validate paths to prevent directory traversal attacks
3. **Performance**: Limit recursion depth and result counts
4. **Documentation**: Keep this README updated with new features

## Troubleshooting

### Common Issues

**Issue**: "Path does not exist"
- **Solution**: Verify the path is correct and accessible

**Issue**: "Permission denied"
- **Solution**: Check file/directory permissions or run with appropriate privileges

**Issue**: "No files found"
- **Solution**: Adjust search pattern or check if files exist in the specified location

**Issue**: Agent not responding
- **Solution**: Restart the function app and verify the agent loads successfully

### Debug Mode

Enable debug logging in `local.settings.json`:

```json
{
    "Values": {
        "LOGGING_LEVEL": "DEBUG"
    }
}
```

## Contributing

To contribute improvements to the Directory Steward Agent:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This agent is part of the Copilot Agent 365 project and follows the same MIT License.

## Support

- **Documentation**: See `/docs` directory for more information
- **Issues**: Report bugs on GitHub Issues
- **Discussions**: Join GitHub Discussions for questions

---

**Created**: 2025-01-16
**Version**: 1.0.0
**Author**: Copilot Agent 365 Team
**Status**: Production Ready ✅
