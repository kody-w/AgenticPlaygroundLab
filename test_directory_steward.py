#!/usr/bin/env python3
"""
Integration test for Directory Steward Agent
Tests the agent within the full function app context
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.directory_steward_agent import DirectoryStewardAgent

def test_agent_initialization():
    """Test agent initializes correctly."""
    print("Testing agent initialization...")
    agent = DirectoryStewardAgent()
    assert agent.name == 'DirectorySteward'
    assert 'name' in agent.metadata
    assert 'description' in agent.metadata
    assert 'parameters' in agent.metadata
    print("✅ Agent initialization test passed")

def test_all_actions():
    """Test all agent actions."""
    agent = DirectoryStewardAgent()
    repo_root = agent.repo_root
    
    actions = [
        ('list_directory', {'action': 'list_directory', 'path': os.path.join(repo_root, 'agents')}),
        ('analyze_structure', {'action': 'analyze_structure', 'path': repo_root, 'depth': 2}),
        ('search_files', {'action': 'search_files', 'path': repo_root, 'pattern': '*.py'}),
        ('get_statistics', {'action': 'get_statistics', 'path': repo_root}),
        ('find_pattern', {'action': 'find_pattern', 'path': repo_root, 'pattern': 'agent'}),
        ('health_check', {'action': 'health_check', 'path': repo_root}),
        ('suggest_maintenance', {'action': 'suggest_maintenance', 'path': repo_root}),
        ('get_file_info', {'action': 'get_file_info', 'path': os.path.join(repo_root, 'README.md')}),
    ]
    
    for action_name, params in actions:
        print(f"\nTesting {action_name}...")
        result = agent.perform(**params)
        assert isinstance(result, str), f"Expected string result for {action_name}"
        assert len(result) > 0, f"Expected non-empty result for {action_name}"
        assert "Error" not in result or "does not exist" not in result, f"Unexpected error in {action_name}: {result[:100]}"
        print(f"✅ {action_name} test passed")

def test_error_handling():
    """Test error handling for invalid inputs."""
    agent = DirectoryStewardAgent()
    
    print("\nTesting error handling...")
    
    # Test invalid path
    result = agent.perform(action='list_directory', path='/nonexistent/path')
    assert "does not exist" in result
    
    # Test invalid action
    result = agent.perform(action='invalid_action')
    assert "Unknown action" in result
    
    print("✅ Error handling test passed")

def test_metadata_schema():
    """Test metadata follows OpenAI function calling schema."""
    agent = DirectoryStewardAgent()
    metadata = agent.metadata
    
    print("\nTesting metadata schema...")
    
    # Check required fields
    assert 'name' in metadata
    assert 'description' in metadata
    assert 'parameters' in metadata
    
    # Check parameters structure
    params = metadata['parameters']
    assert 'type' in params
    assert params['type'] == 'object'
    assert 'properties' in params
    assert 'required' in params
    
    # Check action enum
    action_prop = params['properties']['action']
    assert 'enum' in action_prop
    assert len(action_prop['enum']) == 8
    
    print("✅ Metadata schema test passed")

def main():
    """Run all tests."""
    print("=" * 70)
    print("Directory Steward Agent - Integration Tests")
    print("=" * 70)
    
    try:
        test_agent_initialization()
        test_metadata_schema()
        test_all_actions()
        test_error_handling()
        
        print("\n" + "=" * 70)
        print("🎉 All tests passed successfully!")
        print("=" * 70)
        return 0
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
