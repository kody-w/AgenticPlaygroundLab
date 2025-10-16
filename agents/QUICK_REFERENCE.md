# Directory Steward Agent - Quick Reference

## 🚀 Quick Commands

| What You Want | Say This |
|---------------|----------|
| See directory structure | "Show me the directory structure" |
| Find Python files | "Find all Python files" |
| Get project stats | "Give me statistics about the codebase" |
| Search for code | "Find files containing BasicAgent" |
| Check health | "Check repository health" |
| List folder contents | "List the contents of agents/" |
| File details | "Tell me about function_app.py" |
| Maintenance tips | "What maintenance should I do?" |

## 📋 Available Actions

| Action | Description | Example Parameters |
|--------|-------------|-------------------|
| `analyze_structure` | Visual directory tree | `path`, `depth=3` |
| `search_files` | Find files by pattern | `pattern="*.py"` |
| `get_statistics` | File type statistics | `path` |
| `find_pattern` | Search file contents | `pattern="agent"` |
| `health_check` | Repository health | `path` |
| `list_directory` | List folder contents | `path="/agents"` |
| `get_file_info` | File metadata | `path="/file.py"` |
| `suggest_maintenance` | Maintenance tips | `path` |

## 🎯 Search Patterns

| Pattern | Finds |
|---------|-------|
| `*.py` | All Python files |
| `*.md` | All Markdown files |
| `agent` | Files with "agent" in name |
| `test*` | Files starting with "test" |
| `*config*` | Files containing "config" |

## 💡 Tips

- **Depth Control**: Use `depth=2` for faster results on large repos
- **Path Specific**: Specify paths to narrow scope: `path="/agents"`
- **Natural Language**: Just talk naturally - the agent understands!
- **Combine Actions**: Ask multiple questions in one conversation

## 🔧 API Examples

### REST API
```bash
curl -X POST http://localhost:7071/api/businessinsightbot_function \
  -H "Content-Type: application/json" \
  -d '{"user_input": "Show me the directory structure"}'
```

### Python
```python
from agents.directory_steward_agent import DirectoryStewardAgent

agent = DirectoryStewardAgent()
result = agent.perform(action='analyze_structure', depth=2)
print(result)
```

### Direct Function Call
```json
{
    "action": "search_files",
    "path": "/path/to/search",
    "pattern": "*.py"
}
```

## 📊 Output Features

- 📁 **Icons**: Files and folders have visual icons
- 📏 **Sizes**: Human-readable file sizes (KB, MB)
- 📈 **Statistics**: Percentages and distributions
- 🎨 **Formatting**: Beautiful, easy-to-read output
- ⚠️  **Warnings**: Clear error messages

## 🚫 Smart Filtering

Automatically ignores:
- Hidden files (`.git`, `.venv`)
- Build artifacts (`__pycache__`, `node_modules`)
- Temporary files
- System files

## 📚 Documentation

- **Full Guide**: `agents/README_DIRECTORY_STEWARD.md`
- **Usage Examples**: `agents/USAGE_GUIDE.md`
- **This Reference**: `agents/QUICK_REFERENCE.md`

## ⚡ Performance Tips

1. **Limit Depth**: `depth=2` or `depth=3` for large repos
2. **Specific Paths**: Search in specific directories
3. **Targeted Patterns**: Use specific file patterns
4. **Avoid Root**: Don't search from system root

## 🔐 Security

- ✅ Path validation (stays within repo)
- ✅ Permission error handling
- ✅ Safe file reading
- ✅ No credential exposure

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Path does not exist" | Check path spelling and existence |
| "Permission denied" | Check file permissions |
| "No files found" | Try broader search pattern |
| Agent not responding | Restart function app |

## 🎓 Common Workflows

### New Team Member
1. "Show me the directory structure"
2. "Give me statistics about the codebase"
3. "List the agents directory"

### Code Review
1. "Find all Python files"
2. "Search for files containing TODO"
3. "Check repository health"

### Maintenance
1. "Check repository health"
2. "What maintenance should I do?"
3. "Find large files"

### Documentation
1. "Find all markdown files"
2. "List the docs directory"
3. "Search for README files"

---

**Need more help?** See the full documentation in `agents/README_DIRECTORY_STEWARD.md`
