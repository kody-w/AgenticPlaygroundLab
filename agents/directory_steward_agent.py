"""
Directory Steward Agent - Autonomous Directory Management and Monitoring

This agent provides comprehensive directory stewardship capabilities including:
- Directory structure analysis and visualization
- File search and pattern matching
- Repository health monitoring
- Organization and maintenance suggestions
- File statistics and change tracking
"""

import os
import json
import glob
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from agents.basic_agent import BasicAgent


class DirectoryStewardAgent(BasicAgent):
    """
    Autonomous agent for stewarding and managing directory structures.
    
    This agent can analyze, monitor, and maintain directory organization,
    providing insights and recommendations for repository health.
    """
    
    def __init__(self):
        self.name = 'DirectorySteward'
        self.metadata = {
            "name": self.name,
            "description": (
                "Autonomous directory steward that can analyze directory structures, "
                "search for files, monitor repository health, and provide organizational insights. "
                "Use this agent to get information about files and directories, find patterns, "
                "or get suggestions for maintaining the codebase."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "description": "The action to perform",
                        "enum": [
                            "analyze_structure",
                            "search_files",
                            "get_statistics",
                            "find_pattern",
                            "health_check",
                            "list_directory",
                            "get_file_info",
                            "suggest_maintenance"
                        ]
                    },
                    "path": {
                        "type": "string",
                        "description": "Optional path to analyze or search within. Defaults to repository root."
                    },
                    "pattern": {
                        "type": "string",
                        "description": "File pattern or search term (e.g., '*.py', 'agent', 'test')"
                    },
                    "depth": {
                        "type": "integer",
                        "description": "Maximum depth for directory traversal (default: 3)",
                        "minimum": 1,
                        "maximum": 10
                    }
                },
                "required": ["action"]
            }
        }
        super().__init__(self.name, self.metadata)
        
        # Set the repository root - adjust based on where function_app.py is located
        self.repo_root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        
    def perform(self, **kwargs) -> str:
        """
        Execute the directory stewardship action.
        
        Args:
            action: The action to perform
            path: Optional path parameter
            pattern: Optional search pattern
            depth: Maximum traversal depth
            
        Returns:
            str: Result of the operation
        """
        action = kwargs.get('action', '')
        path = kwargs.get('path', self.repo_root)
        pattern = kwargs.get('pattern', '*')
        depth = kwargs.get('depth', 3)
        
        # Ensure path is absolute and within repo bounds
        if not os.path.isabs(path):
            path = os.path.join(self.repo_root, path)
        
        try:
            if action == 'analyze_structure':
                return self._analyze_structure(path, depth)
            elif action == 'search_files':
                return self._search_files(path, pattern)
            elif action == 'get_statistics':
                return self._get_statistics(path)
            elif action == 'find_pattern':
                return self._find_pattern(path, pattern)
            elif action == 'health_check':
                return self._health_check(path)
            elif action == 'list_directory':
                return self._list_directory(path)
            elif action == 'get_file_info':
                return self._get_file_info(path)
            elif action == 'suggest_maintenance':
                return self._suggest_maintenance(path)
            else:
                return f"Unknown action: {action}. Available actions: analyze_structure, search_files, get_statistics, find_pattern, health_check, list_directory, get_file_info, suggest_maintenance"
        except Exception as e:
            return f"Error performing {action}: {str(e)}"
    
    def _analyze_structure(self, path: str, max_depth: int) -> str:
        """Analyze and visualize directory structure."""
        if not os.path.exists(path):
            return f"Path does not exist: {path}"
        
        if not os.path.isdir(path):
            return f"Path is not a directory: {path}"
        
        result = [f"📁 Directory Structure Analysis: {os.path.basename(path) or path}\n"]
        result.append("=" * 60)
        
        structure = self._build_tree(path, max_depth=max_depth)
        result.append(structure)
        
        # Add summary statistics
        stats = self._count_items(path, max_depth)
        result.append("\n" + "=" * 60)
        result.append(f"\n📊 Summary:")
        result.append(f"  • Total directories: {stats['dirs']}")
        result.append(f"  • Total files: {stats['files']}")
        result.append(f"  • Total size: {self._format_size(stats['size'])}")
        
        return "\n".join(result)
    
    def _build_tree(self, path: str, prefix: str = "", max_depth: int = 3, current_depth: int = 0) -> str:
        """Build a tree representation of directory structure."""
        if current_depth >= max_depth:
            return ""
        
        result = []
        try:
            items = sorted(os.listdir(path))
            # Filter out hidden files and common ignores
            items = [item for item in items if not item.startswith('.') and item not in ['__pycache__', 'node_modules', '.venv']]
            
            for i, item in enumerate(items):
                item_path = os.path.join(path, item)
                is_last = i == len(items) - 1
                connector = "└── " if is_last else "├── "
                
                if os.path.isdir(item_path):
                    result.append(f"{prefix}{connector}📁 {item}/")
                    extension = "    " if is_last else "│   "
                    subtree = self._build_tree(item_path, prefix + extension, max_depth, current_depth + 1)
                    if subtree:
                        result.append(subtree)
                else:
                    icon = self._get_file_icon(item)
                    result.append(f"{prefix}{connector}{icon} {item}")
        except PermissionError:
            result.append(f"{prefix}[Permission Denied]")
        
        return "\n".join(result)
    
    def _get_file_icon(self, filename: str) -> str:
        """Get an appropriate icon for a file based on extension."""
        ext = os.path.splitext(filename)[1].lower()
        icons = {
            '.py': '🐍',
            '.js': '📜',
            '.json': '📋',
            '.md': '📝',
            '.txt': '📄',
            '.html': '🌐',
            '.css': '🎨',
            '.sh': '⚙️',
            '.yml': '⚙️',
            '.yaml': '⚙️',
            '.xml': '📋',
            '.sql': '🗄️',
        }
        return icons.get(ext, '📄')
    
    def _count_items(self, path: str, max_depth: int, current_depth: int = 0) -> Dict[str, int]:
        """Count directories, files, and total size recursively."""
        stats = {'dirs': 0, 'files': 0, 'size': 0}
        
        if current_depth >= max_depth:
            return stats
        
        try:
            for item in os.listdir(path):
                if item.startswith('.') or item in ['__pycache__', 'node_modules', '.venv']:
                    continue
                
                item_path = os.path.join(path, item)
                
                if os.path.isdir(item_path):
                    stats['dirs'] += 1
                    sub_stats = self._count_items(item_path, max_depth, current_depth + 1)
                    stats['dirs'] += sub_stats['dirs']
                    stats['files'] += sub_stats['files']
                    stats['size'] += sub_stats['size']
                else:
                    stats['files'] += 1
                    try:
                        stats['size'] += os.path.getsize(item_path)
                    except:
                        pass
        except PermissionError:
            pass
        
        return stats
    
    def _search_files(self, path: str, pattern: str) -> str:
        """Search for files matching a pattern."""
        if not os.path.exists(path):
            return f"Path does not exist: {path}"
        
        results = []
        # Handle different pattern formats
        if pattern.startswith('*.'):
            search_pattern = f"**/{pattern}"  # Extension pattern
        elif '*' in pattern:
            search_pattern = f"**/{pattern}"  # Already has wildcards
        else:
            search_pattern = f"**/*{pattern}*"  # Simple name search
        
        try:
            matches = list(Path(path).glob(search_pattern))
            
            # Filter out unwanted directories
            matches = [m for m in matches if not any(
                part.startswith('.') or part in ['__pycache__', 'node_modules', '.venv']
                for part in m.parts
            )]
            
            if not matches:
                return f"No files found matching pattern: {pattern}"
            
            results.append(f"🔍 Search Results for '{pattern}' in {os.path.basename(path)}:\n")
            results.append("=" * 60)
            
            # Group by type
            files = [m for m in matches if m.is_file()]
            dirs = [m for m in matches if m.is_dir()]
            
            if dirs:
                results.append(f"\n📁 Directories ({len(dirs)}):")
                for d in sorted(dirs)[:20]:  # Limit to 20
                    rel_path = os.path.relpath(d, path)
                    results.append(f"  • {rel_path}")
                if len(dirs) > 20:
                    results.append(f"  ... and {len(dirs) - 20} more")
            
            if files:
                results.append(f"\n📄 Files ({len(files)}):")
                for f in sorted(files)[:30]:  # Limit to 30
                    rel_path = os.path.relpath(f, path)
                    size = self._format_size(f.stat().st_size)
                    results.append(f"  • {rel_path} ({size})")
                if len(files) > 30:
                    results.append(f"  ... and {len(files) - 30} more")
            
            return "\n".join(results)
        
        except Exception as e:
            return f"Error searching files: {str(e)}"
    
    def _get_statistics(self, path: str) -> str:
        """Get detailed statistics about the directory."""
        if not os.path.exists(path):
            return f"Path does not exist: {path}"
        
        results = [f"📊 Directory Statistics: {os.path.basename(path) or path}\n"]
        results.append("=" * 60)
        
        # File type counts
        extensions = {}
        total_files = 0
        total_size = 0
        
        for root, dirs, files in os.walk(path):
            # Skip hidden and unwanted directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules', '.venv']]
            
            for file in files:
                if file.startswith('.'):
                    continue
                
                total_files += 1
                ext = os.path.splitext(file)[1] or 'no extension'
                extensions[ext] = extensions.get(ext, 0) + 1
                
                try:
                    file_path = os.path.join(root, file)
                    total_size += os.path.getsize(file_path)
                except:
                    pass
        
        results.append(f"\n📁 Overview:")
        results.append(f"  • Total files: {total_files}")
        results.append(f"  • Total size: {self._format_size(total_size)}")
        
        if extensions:
            results.append(f"\n📋 File Types (Top 10):")
            sorted_exts = sorted(extensions.items(), key=lambda x: x[1], reverse=True)[:10]
            for ext, count in sorted_exts:
                percentage = (count / total_files) * 100
                results.append(f"  • {ext}: {count} files ({percentage:.1f}%)")
        
        return "\n".join(results)
    
    def _find_pattern(self, path: str, pattern: str) -> str:
        """Find files containing a specific content pattern."""
        if not os.path.exists(path):
            return f"Path does not exist: {path}"
        
        results = []
        matches = []
        
        try:
            for root, dirs, files in os.walk(path):
                # Skip hidden and unwanted directories
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules', '.venv']]
                
                for file in files:
                    # Only search in text files
                    if not file.endswith(('.py', '.js', '.json', '.md', '.txt', '.html', '.css', '.yml', '.yaml', '.sh')):
                        continue
                    
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            if pattern.lower() in content.lower():
                                rel_path = os.path.relpath(file_path, path)
                                # Count occurrences
                                count = content.lower().count(pattern.lower())
                                matches.append((rel_path, count))
                    except:
                        continue
            
            if not matches:
                return f"No files found containing pattern: '{pattern}'"
            
            results.append(f"🔎 Pattern Search Results for '{pattern}':\n")
            results.append("=" * 60)
            results.append(f"\nFound in {len(matches)} files:\n")
            
            # Sort by occurrence count
            matches.sort(key=lambda x: x[1], reverse=True)
            
            for rel_path, count in matches[:20]:  # Limit to 20
                results.append(f"  • {rel_path} ({count} occurrence{'s' if count > 1 else ''})")
            
            if len(matches) > 20:
                results.append(f"\n  ... and {len(matches) - 20} more files")
            
            return "\n".join(results)
        
        except Exception as e:
            return f"Error searching for pattern: {str(e)}"
    
    def _health_check(self, path: str) -> str:
        """Perform a health check on the repository."""
        if not os.path.exists(path):
            return f"Path does not exist: {path}"
        
        results = [f"🏥 Repository Health Check: {os.path.basename(path) or path}\n"]
        results.append("=" * 60)
        
        issues = []
        suggestions = []
        
        # Check for common issues
        # 1. Large files
        large_files = []
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules', '.venv']]
            
            for file in files:
                if file.startswith('.'):
                    continue
                file_path = os.path.join(root, file)
                try:
                    size = os.path.getsize(file_path)
                    if size > 10 * 1024 * 1024:  # > 10MB
                        rel_path = os.path.relpath(file_path, path)
                        large_files.append((rel_path, size))
                except:
                    pass
        
        if large_files:
            issues.append(f"⚠️  Found {len(large_files)} large files (>10MB)")
            for file_path, size in sorted(large_files, key=lambda x: x[1], reverse=True)[:5]:
                issues.append(f"    • {file_path} ({self._format_size(size)})")
        
        # 2. Check for important files
        important_files = ['README.md', 'requirements.txt', '.gitignore', 'LICENSE']
        missing_files = []
        for file in important_files:
            if not os.path.exists(os.path.join(path, file)):
                missing_files.append(file)
        
        if missing_files:
            suggestions.append(f"💡 Consider adding: {', '.join(missing_files)}")
        
        # 3. Check for empty directories
        empty_dirs = []
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            if not dirs and not files:
                rel_path = os.path.relpath(root, path)
                empty_dirs.append(rel_path)
        
        if empty_dirs:
            suggestions.append(f"🗑️  Found {len(empty_dirs)} empty directories that could be cleaned up")
        
        # Output results
        if not issues and not suggestions:
            results.append("\n✅ Repository is in good health!")
            results.append("\nNo issues or suggestions found.")
        else:
            if issues:
                results.append("\n⚠️  Issues Found:")
                for issue in issues:
                    results.append(issue)
            
            if suggestions:
                results.append("\n💡 Suggestions:")
                for suggestion in suggestions:
                    results.append(suggestion)
        
        return "\n".join(results)
    
    def _list_directory(self, path: str) -> str:
        """List contents of a specific directory."""
        if not os.path.exists(path):
            return f"Path does not exist: {path}"
        
        if not os.path.isdir(path):
            return f"Path is not a directory: {path}"
        
        try:
            items = os.listdir(path)
            
            results = [f"📂 Contents of {os.path.basename(path) or path}:\n"]
            results.append("=" * 60)
            
            dirs = []
            files = []
            
            for item in sorted(items):
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    dirs.append(item)
                else:
                    size = os.path.getsize(item_path)
                    files.append((item, size))
            
            if dirs:
                results.append(f"\n📁 Directories ({len(dirs)}):")
                for d in dirs:
                    results.append(f"  • {d}/")
            
            if files:
                results.append(f"\n📄 Files ({len(files)}):")
                for file, size in files:
                    results.append(f"  • {file} ({self._format_size(size)})")
            
            if not dirs and not files:
                results.append("\nDirectory is empty.")
            
            return "\n".join(results)
        
        except PermissionError:
            return f"Permission denied accessing: {path}"
        except Exception as e:
            return f"Error listing directory: {str(e)}"
    
    def _get_file_info(self, path: str) -> str:
        """Get detailed information about a file."""
        if not os.path.exists(path):
            return f"Path does not exist: {path}"
        
        try:
            stats = os.stat(path)
            
            results = [f"📄 File Information: {os.path.basename(path)}\n"]
            results.append("=" * 60)
            results.append(f"\n📍 Path: {path}")
            results.append(f"📏 Size: {self._format_size(stats.st_size)}")
            results.append(f"📅 Modified: {datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')}")
            results.append(f"📅 Created: {datetime.fromtimestamp(stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S')}")
            
            if os.path.isfile(path):
                ext = os.path.splitext(path)[1]
                results.append(f"📋 Type: {ext or 'No extension'}")
                
                # Try to get line count for text files
                if ext in ['.py', '.js', '.json', '.md', '.txt', '.html', '.css', '.yml', '.yaml']:
                    try:
                        with open(path, 'r', encoding='utf-8') as f:
                            lines = len(f.readlines())
                        results.append(f"📝 Lines: {lines}")
                    except:
                        pass
            
            return "\n".join(results)
        
        except Exception as e:
            return f"Error getting file info: {str(e)}"
    
    def _suggest_maintenance(self, path: str) -> str:
        """Suggest maintenance tasks for the repository."""
        if not os.path.exists(path):
            return f"Path does not exist: {path}"
        
        results = [f"🔧 Maintenance Suggestions for {os.path.basename(path) or path}\n"]
        results.append("=" * 60)
        
        suggestions = []
        
        # Check agent organization
        agents_dir = os.path.join(path, 'agents')
        if os.path.exists(agents_dir):
            agent_files = [f for f in os.listdir(agents_dir) if f.endswith('_agent.py')]
            if agent_files:
                suggestions.append(f"✅ Found {len(agent_files)} agent files in agents/ directory")
            else:
                suggestions.append("💡 No agent files found in agents/ directory")
        
        # Check documentation
        docs_dir = os.path.join(path, 'docs')
        if os.path.exists(docs_dir):
            doc_files = [f for f in os.listdir(docs_dir) if f.endswith('.md')]
            suggestions.append(f"📚 Documentation: {len(doc_files)} markdown files in docs/")
        else:
            suggestions.append("💡 Consider creating a docs/ directory for documentation")
        
        # Check for tests
        test_files = []
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            test_files.extend([f for f in files if 'test' in f.lower()])
        
        if test_files:
            suggestions.append(f"✅ Found {len(test_files)} test-related files")
        else:
            suggestions.append("💡 Consider adding tests for better code quality")
        
        # Check for configuration files
        config_files = ['local.settings.json', 'requirements.txt', 'package.json']
        found_configs = [f for f in config_files if os.path.exists(os.path.join(path, f))]
        if found_configs:
            suggestions.append(f"✅ Configuration files found: {', '.join(found_configs)}")
        
        # General suggestions
        suggestions.append("\n🎯 General Recommendations:")
        suggestions.append("  • Keep agents in the agents/ directory")
        suggestions.append("  • Document each agent's purpose and usage")
        suggestions.append("  • Regularly review and update dependencies")
        suggestions.append("  • Maintain consistent code style")
        suggestions.append("  • Use version control for all changes")
        
        results.append("\n" + "\n".join(suggestions))
        
        return "\n".join(results)
    
    def _format_size(self, size: int) -> str:
        """Format size in bytes to human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} PB"
