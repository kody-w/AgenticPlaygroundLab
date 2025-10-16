from agents.basic_agent import BasicAgent
from utils.azure_file_storage import AzureFileStorageManager
import json
import re
import logging
from datetime import datetime

class MetaAgent(BasicAgent):
    def __init__(self):
        self.name = 'MetaAgent'
        self.metadata = {
            "name": self.name,
            "description": "Generates and saves custom sub-agents dynamically based on user requirements. This agent can create new specialized agents with custom functionality and save them to Azure File Storage for immediate use.",
            "parameters": {
                "type": "object",
                "properties": {
                    "agent_name": {
                        "type": "string",
                        "description": "The name of the agent to create (e.g., 'WeatherFetcher', 'DataAnalyzer'). Should be CamelCase without spaces."
                    },
                    "agent_description": {
                        "type": "string",
                        "description": "A clear description of what the agent does and when it should be used."
                    },
                    "parameters": {
                        "type": "object",
                        "description": "The input parameters the agent needs. Each key should be a parameter name with properties: 'type' (string/integer/array/object/boolean), 'description', and optionally 'required' (boolean).",
                        "additionalProperties": True
                    },
                    "implementation_logic": {
                        "type": "string",
                        "description": "Detailed description of the logic and behavior the agent should implement. This will be used to generate the perform() method."
                    },
                    "required_imports": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional. List of Python imports needed (e.g., ['import json', 'from datetime import datetime'])"
                    }
                },
                "required": ["agent_name", "agent_description", "implementation_logic"]
            }
        }
        self.storage_manager = AzureFileStorageManager()
        super().__init__(name=self.name, metadata=self.metadata)
    
    def _sanitize_agent_name(self, name):
        """Ensure agent name is valid Python class name"""
        # Remove any non-alphanumeric characters except underscores
        name = re.sub(r'[^\w]', '', name)
        # Ensure it starts with a letter
        if name and not name[0].isalpha():
            name = 'Agent' + name
        # Convert to CamelCase if needed
        if '_' in name:
            name = ''.join(word.capitalize() for word in name.split('_'))
        return name or 'CustomAgent'
    
    def _build_parameters_schema(self, parameters):
        """Build OpenAI function parameters schema from user input"""
        if not parameters:
            return {
                "type": "object",
                "properties": {},
                "required": []
            }
        
        properties = {}
        required = []
        
        for param_name, param_info in parameters.items():
            if isinstance(param_info, dict):
                prop = {
                    "type": param_info.get("type", "string"),
                    "description": param_info.get("description", f"Parameter {param_name}")
                }
                
                # Handle enum values if provided
                if "enum" in param_info:
                    prop["enum"] = param_info["enum"]
                
                # Handle array items if type is array
                if prop["type"] == "array" and "items" in param_info:
                    prop["items"] = param_info["items"]
                
                # Handle additional properties for object types
                if prop["type"] == "object":
                    if "properties" in param_info:
                        prop["properties"] = param_info["properties"]
                    if "additionalProperties" in param_info:
                        prop["additionalProperties"] = param_info["additionalProperties"]
                
                properties[param_name] = prop
                
                # Check if required
                if param_info.get("required", False):
                    required.append(param_name)
            else:
                # Simple parameter definition
                properties[param_name] = {
                    "type": "string",
                    "description": str(param_info)
                }
        
        return {
            "type": "object",
            "properties": properties,
            "required": required
        }
    
    def _generate_perform_method(self, parameters, implementation_logic):
        """Generate the perform method implementation"""
        # Extract parameter names
        param_names = list(parameters.keys()) if parameters else []
        
        # Build parameter extraction code
        param_extractions = []
        for param_name in param_names:
            param_info = parameters[param_name]
            default_value = "''" if param_info.get("type") == "string" else "None"
            if param_info.get("type") == "array":
                default_value = "[]"
            elif param_info.get("type") == "integer":
                default_value = "0"
            elif param_info.get("type") == "boolean":
                default_value = "False"
            param_extractions.append(f"        {param_name} = kwargs.get('{param_name}', {default_value})")
        
        param_extraction_code = "\n".join(param_extractions) if param_extractions else "        pass"
        
        # Clean up implementation logic for docstring - replace newlines and extra spaces
        clean_logic = " ".join(implementation_logic.split())
        
        # Generate implementation based on logic description
        implementation = f'''    def perform(self, **kwargs):
        """
        Implementation logic: {clean_logic}
        """
{param_extraction_code}
        
        try:
            # TODO: Implement the actual logic based on the description above
            # This is a generated template - customize the implementation as needed
            
            result = {{
                "status": "success",
                "message": "Agent executed successfully",
                "inputs": {{{', '.join([f'"{p}": {p}' for p in param_names])}}}
            }}
            
            return json.dumps(result)
            
        except Exception as e:
            return json.dumps({{
                "status": "error",
                "message": f"Error in agent execution: {{str(e)}}"
            }})
'''
        return implementation
    
    def _generate_agent_code(self, agent_name, agent_description, parameters, 
                            implementation_logic, required_imports=None):
        """Generate complete agent Python code"""
        sanitized_name = self._sanitize_agent_name(agent_name)
        
        # Build imports
        imports = ["from agents.basic_agent import BasicAgent", "import json"]
        if required_imports:
            for imp in required_imports:
                if imp not in imports:
                    imports.append(imp)
        
        imports_code = "\n".join(imports)
        
        # Build parameters schema
        params_schema = self._build_parameters_schema(parameters)
        
        # Generate perform method
        perform_method = self._generate_perform_method(parameters, implementation_logic)
        
        # Build complete agent code
        agent_code = f'''"""
Auto-generated agent: {sanitized_name}
Description: {agent_description}
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

{imports_code}

class {sanitized_name}(BasicAgent):
    def __init__(self):
        self.name = '{sanitized_name}'
        self.metadata = {{
            "name": self.name,
            "description": "{agent_description}",
            "parameters": {json.dumps(params_schema, indent=16)}
        }}
        super().__init__(name=self.name, metadata=self.metadata)
    
{perform_method}
'''
        return agent_code, sanitized_name
    
    def _validate_agent_code(self, code):
        """Basic validation of generated agent code"""
        try:
            # Check for basic syntax errors
            compile(code, '<string>', 'exec')
            
            # Check for required components
            if 'class' not in code:
                return False, "Generated code missing class definition"
            if 'BasicAgent' not in code:
                return False, "Generated code doesn't inherit from BasicAgent"
            if 'def perform' not in code:
                return False, "Generated code missing perform method"
            
            return True, "Code validation passed"
        except SyntaxError as e:
            return False, f"Syntax error in generated code: {str(e)}"
        except Exception as e:
            return False, f"Validation error: {str(e)}"
    
    def perform(self, **kwargs):
        """
        Generate a new agent and save it to Azure File Storage.
        """
        agent_name = kwargs.get('agent_name', '')
        agent_description = kwargs.get('agent_description', '')
        parameters = kwargs.get('parameters', {})
        implementation_logic = kwargs.get('implementation_logic', '')
        required_imports = kwargs.get('required_imports', [])
        
        # Validate inputs
        if not agent_name:
            return json.dumps({
                "status": "error",
                "message": "Agent name is required"
            })
        
        if not agent_description:
            return json.dumps({
                "status": "error",
                "message": "Agent description is required"
            })
        
        if not implementation_logic:
            return json.dumps({
                "status": "error",
                "message": "Implementation logic description is required"
            })
        
        try:
            # Generate agent code
            agent_code, sanitized_name = self._generate_agent_code(
                agent_name, 
                agent_description, 
                parameters,
                implementation_logic,
                required_imports
            )
            
            # Validate generated code
            is_valid, validation_msg = self._validate_agent_code(agent_code)
            if not is_valid:
                return json.dumps({
                    "status": "error",
                    "message": f"Generated code validation failed: {validation_msg}",
                    "generated_code": agent_code
                })
            
            # Save to Azure File Storage in the multi_agents folder
            file_name = f"{sanitized_name.lower()}_agent.py"
            success = self.storage_manager.write_file('multi_agents', file_name, agent_code)
            
            if success:
                return json.dumps({
                    "status": "success",
                    "message": f"Successfully generated and saved agent '{sanitized_name}'",
                    "agent_name": sanitized_name,
                    "file_name": file_name,
                    "location": "multi_agents folder in Azure File Storage",
                    "note": "The agent will be automatically loaded on next function restart",
                    "generated_code_preview": agent_code[:500] + "..." if len(agent_code) > 500 else agent_code
                })
            else:
                return json.dumps({
                    "status": "error",
                    "message": "Failed to save agent to Azure File Storage",
                    "generated_code": agent_code
                })
                
        except Exception as e:
            logging.error(f"Error in MetaAgent: {str(e)}")
            return json.dumps({
                "status": "error",
                "message": f"Error generating agent: {str(e)}"
            })
