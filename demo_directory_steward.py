#!/usr/bin/env python3
"""
Directory Steward Agent - Demonstration Script
Shows all capabilities of the autonomous directory steward
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.directory_steward_agent import DirectoryStewardAgent

def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")

def demo_analyze_structure():
    """Demonstrate directory structure analysis."""
    print_header("DEMO 1: Analyze Directory Structure")
    agent = DirectoryStewardAgent()
    result = agent.perform(
        action='analyze_structure',
        path=agent.repo_root,
        depth=2
    )
    print(result)
    input("\nPress Enter to continue...")

def demo_search_files():
    """Demonstrate file search."""
    print_header("DEMO 2: Search for Python Files")
    agent = DirectoryStewardAgent()
    result = agent.perform(
        action='search_files',
        pattern='*.py'
    )
    print(result)
    input("\nPress Enter to continue...")

def demo_statistics():
    """Demonstrate statistics generation."""
    print_header("DEMO 3: Get Repository Statistics")
    agent = DirectoryStewardAgent()
    result = agent.perform(
        action='get_statistics'
    )
    print(result)
    input("\nPress Enter to continue...")

def demo_find_pattern():
    """Demonstrate content search."""
    print_header("DEMO 4: Find Pattern in Files")
    agent = DirectoryStewardAgent()
    result = agent.perform(
        action='find_pattern',
        pattern='BasicAgent'
    )
    print(result)
    input("\nPress Enter to continue...")

def demo_health_check():
    """Demonstrate health check."""
    print_header("DEMO 5: Repository Health Check")
    agent = DirectoryStewardAgent()
    result = agent.perform(
        action='health_check'
    )
    print(result)
    input("\nPress Enter to continue...")

def demo_list_directory():
    """Demonstrate directory listing."""
    print_header("DEMO 6: List Agents Directory")
    agent = DirectoryStewardAgent()
    agents_path = os.path.join(agent.repo_root, 'agents')
    result = agent.perform(
        action='list_directory',
        path=agents_path
    )
    print(result)
    input("\nPress Enter to continue...")

def demo_file_info():
    """Demonstrate file info."""
    print_header("DEMO 7: Get File Information")
    agent = DirectoryStewardAgent()
    readme_path = os.path.join(agent.repo_root, 'README.md')
    result = agent.perform(
        action='get_file_info',
        path=readme_path
    )
    print(result)
    input("\nPress Enter to continue...")

def demo_maintenance():
    """Demonstrate maintenance suggestions."""
    print_header("DEMO 8: Maintenance Suggestions")
    agent = DirectoryStewardAgent()
    result = agent.perform(
        action='suggest_maintenance'
    )
    print(result)
    input("\nPress Enter to continue...")

def main():
    """Run all demonstrations."""
    print("\n" + "=" * 70)
    print("  🏛️  DIRECTORY STEWARD AGENT - INTERACTIVE DEMONSTRATION")
    print("=" * 70)
    print("\nThis demo showcases all 8 capabilities of the Directory Steward Agent.")
    print("The agent provides autonomous directory management and monitoring.\n")
    
    demos = [
        ("1. Analyze Structure", demo_analyze_structure),
        ("2. Search Files", demo_search_files),
        ("3. Get Statistics", demo_statistics),
        ("4. Find Pattern", demo_find_pattern),
        ("5. Health Check", demo_health_check),
        ("6. List Directory", demo_list_directory),
        ("7. File Info", demo_file_info),
        ("8. Maintenance Suggestions", demo_maintenance),
    ]
    
    print("Available demonstrations:")
    for name, _ in demos:
        print(f"  {name}")
    
    print("\n" + "-" * 70)
    choice = input("\nEnter demo number (1-8) or 'all' to run all demos: ").strip().lower()
    
    if choice == 'all':
        for name, demo_func in demos:
            try:
                demo_func()
            except KeyboardInterrupt:
                print("\n\nDemo interrupted by user.")
                break
            except Exception as e:
                print(f"\n❌ Error in demo: {str(e)}")
                import traceback
                traceback.print_exc()
    elif choice.isdigit() and 1 <= int(choice) <= 8:
        demo_num = int(choice) - 1
        name, demo_func = demos[demo_num]
        try:
            demo_func()
        except Exception as e:
            print(f"\n❌ Error in demo: {str(e)}")
            import traceback
            traceback.print_exc()
    else:
        print("Invalid choice. Please run again and select 1-8 or 'all'.")
        return 1
    
    print("\n" + "=" * 70)
    print("  ✅ DEMONSTRATION COMPLETE")
    print("=" * 70)
    print("\nThe Directory Steward Agent is ready to autonomously steward your directory!")
    print("\nFor more information:")
    print("  • Full Documentation: agents/README_DIRECTORY_STEWARD.md")
    print("  • Usage Examples: agents/USAGE_GUIDE.md")
    print("  • Quick Reference: agents/QUICK_REFERENCE.md")
    print("  • Architecture: agents/ARCHITECTURE.md")
    print("\n")
    
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user. Goodbye!")
        sys.exit(0)
