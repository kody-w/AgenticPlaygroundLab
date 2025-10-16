# Directory Steward Agent - Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      User Interaction Layer                      │
├─────────────────────────────────────────────────────────────────┤
│  Natural Language: "Show me the directory structure"            │
│  OR                                                              │
│  Direct API: {"action": "analyze_structure", "depth": 3}        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Azure Function App Layer                      │
├─────────────────────────────────────────────────────────────────┤
│  function_app.py                                                 │
│  ├── Load agents (including DirectorySteward)                   │
│  ├── Parse user input with GPT-4                                │
│  ├── Identify agent to call                                     │
│  └── Execute agent.perform(**kwargs)                            │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│               Directory Steward Agent Layer                      │
├─────────────────────────────────────────────────────────────────┤
│  DirectoryStewardAgent.perform(action, path, pattern, depth)    │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Action Router                                              │ │
│  │ ├── analyze_structure → _analyze_structure()              │ │
│  │ ├── search_files      → _search_files()                   │ │
│  │ ├── get_statistics    → _get_statistics()                 │ │
│  │ ├── find_pattern      → _find_pattern()                   │ │
│  │ ├── health_check      → _health_check()                   │ │
│  │ ├── list_directory    → _list_directory()                 │ │
│  │ ├── get_file_info     → _get_file_info()                  │ │
│  │ └── suggest_maintenance → _suggest_maintenance()          │ │
│  └────────────────────────────────────────────────────────────┘ │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    File System Layer                             │
├─────────────────────────────────────────────────────────────────┤
│  Python os, pathlib, glob modules                                │
│  ├── Walk directories                                            │
│  ├── Read file metadata                                          │
│  ├── Search patterns                                             │
│  └── Analyze contents                                            │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Agent Initialization

```python
class DirectoryStewardAgent(BasicAgent):
    def __init__(self):
        # Set agent name and metadata
        self.name = 'DirectorySteward'
        self.metadata = {
            "name": self.name,
            "description": "...",
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {"enum": [...]},
                    "path": {...},
                    "pattern": {...},
                    "depth": {...}
                }
            }
        }
        # Initialize with repository root
        self.repo_root = os.path.abspath(...)
```

### 2. Request Flow

```
User Request → GPT-4 Processing → Function Selection → Agent Execution → Response
     │              │                    │                   │              │
     │              │                    │                   │              │
Natural        Understands          Identifies         Performs         Formatted
Language       intent and           DirectorySteward   action with      results with
input          generates            agent with         parameters       icons & stats
               function call        parameters
```

### 3. Action Processing

Each action follows this pattern:

```python
def _action_name(self, path: str, **kwargs) -> str:
    # 1. Validate inputs
    if not os.path.exists(path):
        return "Error message"
    
    # 2. Perform operation
    results = []
    # ... processing logic ...
    
    # 3. Format output
    results.append("Header")
    results.append("=" * 60)
    results.append("Content")
    
    # 4. Return formatted string
    return "\n".join(results)
```

### 4. File System Operations

The agent uses several strategies for file operations:

#### Tree Building
```
_build_tree() → Recursive directory traversal
              → Filter ignored patterns
              → Format with icons and indentation
              → Return visual tree structure
```

#### File Searching
```
_search_files() → Convert pattern to glob format
                → Use pathlib.glob() for matching
                → Filter unwanted directories
                → Group by type (dirs/files)
                → Return sorted results
```

#### Content Searching
```
_find_pattern() → Walk directory tree
                → Read text files only
                → Search for pattern (case-insensitive)
                → Count occurrences
                → Return sorted by frequency
```

#### Statistics
```
_get_statistics() → Count files by extension
                  → Sum total sizes
                  → Calculate percentages
                  → Return top 10 types
```

## Data Flow

### Example: Analyze Structure Request

```
1. User Input
   "Show me the directory structure"
   
2. GPT-4 Function Call
   {
     "name": "DirectorySteward",
     "arguments": {
       "action": "analyze_structure",
       "path": "/repo",
       "depth": 3
     }
   }

3. Agent Execution
   DirectoryStewardAgent.perform(
     action='analyze_structure',
     path='/repo',
     depth=3
   )
   
4. Internal Processing
   _analyze_structure(path, depth)
   ├── _build_tree(path, depth) → Visual tree
   ├── _count_items(path, depth) → Statistics
   └── Format output
   
5. Response
   📁 Directory Structure Analysis: repo
   ==================================
   ├── 📁 agents/
   │   ├── 🐍 agent1.py
   │   └── 🐍 agent2.py
   └── 🐍 main.py
   
   📊 Summary:
   • Total directories: 1
   • Total files: 3
   • Total size: 45.2 KB
```

## Security Architecture

### Path Validation
```
User Input → Normalize Path → Validate Within Bounds → Execute
                                      ↓
                              If outside bounds: Reject
```

### Permission Handling
```
File Access Attempt → Try/Except Block → Handle Gracefully
                                              ↓
                                     [Permission Denied] message
```

### File Reading Safety
```
Open File → Check if text file → Try UTF-8 → Fallback ignore errors
                 ↓                                   ↓
            Skip binary files              Continue with errors handled
```

## Performance Optimizations

### 1. Depth Limiting
```
Current Depth < Max Depth → Continue Traversal
                   ↓
Current Depth >= Max Depth → Stop and Return
```

### 2. Smart Filtering
```
Check Directory Name → Is in ignore list? → Skip
                                ↓
                           Not ignored → Process
```

### 3. Result Limiting
```
Collect Results → Limit to N items → Show "...and X more"
```

### 4. Lazy Loading
```
Only read file contents when specifically requested
Don't load binary files unless needed
Cache common operations
```

## Integration Points

### With Function App
```
function_app.py
  ├── load_agents_from_folder()
  │   └── Imports DirectoryStewardAgent
  ├── Assistant.__init__()
  │   └── Stores agent in known_agents dict
  └── Assistant.generate_response()
      └── Calls agent.perform() when selected
```

### With Azure OpenAI
```
User Message → Assistant.generate_response()
                   ↓
              GPT-4 with function definitions
                   ↓
              Returns function call
                   ↓
              Execute DirectorySteward.perform()
                   ↓
              Send result back to GPT-4
                   ↓
              GPT-4 formats final response
```

### With Other Agents
```
User: "Find all agent files and tell me what they do"
  ├── DirectorySteward.search_files(pattern="*agent*.py")
  ├── ContextMemoryAgent.recall(agent documentation)
  └── GPT-4 combines both responses
```

## Error Handling Flow

```
User Request
    ↓
Validate Parameters
    ↓
├─ Valid? → Execute Action
│              ↓
│          Try Block
│              ↓
│          ├─ Success? → Format & Return
│          └─ Exception? → Catch & Return Error Message
│
└─ Invalid? → Return Validation Error
```

## Deployment

### Local Development
```
1. Agent file in agents/ directory
2. Function app loads on startup
3. Agent available immediately
4. Test with: func start
```

### Azure Deployment
```
1. Include in deployment package
2. Upload to Azure Functions
3. Function app restarts
4. Agent auto-loads
5. Available through API endpoint
```

### Azure Storage Deployment
```
1. Upload to storage agents/ share
2. Function app loads from storage
3. No function restart required
4. Dynamic agent updates
```

## Monitoring

### Logging Points
```
- Agent initialization
- Action execution start
- File access errors
- Pattern match counts
- Action completion
- Error occurrences
```

### Performance Metrics
```
- Execution time per action
- Files processed count
- Directory traversal depth
- Result set sizes
- Error rates
```

## Extension Points

### Adding New Actions
```
1. Add to metadata enum
2. Implement _new_action() method
3. Add dispatch in perform()
4. Test thoroughly
5. Document in README
```

### Customizing Behavior
```
- Modify ignore patterns
- Change output formatting
- Adjust size limits
- Customize icons
- Add new file type handlers
```

---

This architecture ensures:
- ✅ Modularity (easy to extend)
- ✅ Security (path validation)
- ✅ Performance (optimized traversal)
- ✅ Reliability (error handling)
- ✅ Usability (natural language)
