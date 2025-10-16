import logging
import re
from agents.basic_agent import BasicAgent
from utils.azure_file_storage import AzureFileStorageManager
from openai import AzureOpenAI
import os

class MetaAgent(BasicAgent):
    """
    A meta agent that generates and saves custom sub-agents based on user requirements.
    This agent uses AI to create fully functional agent code that can be persisted and reused.
    """
    
    def __init__(self):
        self.name = 'MetaAgent'
        self.metadata = {
            "name": self.name,
            "description": "Generates and saves custom sub-agents based on specific requirements. This agent creates new specialized agents on-demand and stores them for future use.",
            "parameters": {
                "type": "object",
                "properties": {
                    "agent_name": {
                        "type": "string",
                        "description": "A descriptive name for the new agent (will be converted to PascalCase, e.g., 'SalesAnalysis' or 'CustomerService')"
                    },
                    "agent_description": {
                        "type": "string",
                        "description": "A detailed description of what the agent should do, including its purpose, functionality, and expected behavior"
                    },
                    "parameters": {
                        "type": "string",
                        "description": "Optional: JSON-formatted string describing the parameters the agent should accept (e.g., '{\"query\": \"search term\", \"limit\": \"number of results\"}')"
                    },
                    "agent_type": {
                        "type": "string",
                        "enum": ["single", "multi"],
                        "description": "Type of agent to create: 'single' for standalone agents, 'multi' for multi-agent orchestrators that coordinate other agents"
                    }
                },
                "required": ["agent_name", "agent_description"]
            }
        }
        self.storage_manager = AzureFileStorageManager()
        
        # Initialize Azure OpenAI client for code generation
        try:
            api_key = os.environ.get('AZURE_OPENAI_API_KEY')
            endpoint = os.environ.get('AZURE_OPENAI_ENDPOINT')
            api_version = os.environ.get('AZURE_OPENAI_API_VERSION', '2024-02-01')
            
            if not api_key or not endpoint:
                raise ValueError("Azure OpenAI API key and endpoint are required")
            
            self.client = AzureOpenAI(
                api_key=api_key,
                api_version=api_version,
                azure_endpoint=endpoint
            )
            self.deployment_name = os.environ.get('AZURE_OPENAI_DEPLOYMENT_NAME', 'gpt-deployment')
        except Exception as e:
            logging.error(f"Failed to initialize Azure OpenAI client in MetaAgent: {str(e)}")
            self.client = None
        
        super().__init__(name=self.name, metadata=self.metadata)
        
    def perform(self, **kwargs):
        """
        Generate and save a custom agent based on the provided requirements.
        
        Args:
            agent_name: Name for the new agent
            agent_description: Description of what the agent should do
            parameters: Optional parameter definitions
            agent_type: Type of agent ('single' or 'multi')
        
        Returns:
            Status message indicating success or failure
        """
        agent_name = kwargs.get('agent_name')
        agent_description = kwargs.get('agent_description')
        parameters = kwargs.get('parameters', '')
        agent_type = kwargs.get('agent_type', 'single')
        
        if not agent_name or not agent_description:
            return "Error: Both agent_name and agent_description are required to generate an agent."
        
        # Validate agent type
        if agent_type not in ['single', 'multi']:
            agent_type = 'single'
        
        # Convert agent name to valid Python class name
        class_name = self._to_pascal_case(agent_name)
        file_name = self._to_snake_case(agent_name) + '_agent.py'
        
        try:
            # Generate the agent code
            agent_code = self._generate_agent_code(
                class_name, 
                agent_description, 
                parameters,
                agent_type
            )
            
            if not agent_code:
                return "Error: Failed to generate agent code. The AI service may be unavailable."
            
            # Validate the generated code
            validation_error = self._validate_agent_code(agent_code)
            if validation_error:
                return f"Error: Generated agent code is invalid: {validation_error}"
            
            # Determine which folder to save to
            folder_name = 'multi_agents' if agent_type == 'multi' else 'agents'
            
            # Save the agent to Azure File Storage
            success = self.storage_manager.write_file(folder_name, file_name, agent_code)
            
            if success:
                return f"✅ Successfully created and saved agent '{class_name}'!\n\n" \
                       f"📁 Location: {folder_name}/{file_name}\n" \
                       f"🔄 The agent will be available after reloading the system.\n\n" \
                       f"Agent Type: {agent_type.upper()}\n" \
                       f"Description: {agent_description}"
            else:
                return f"Error: Failed to save agent to Azure File Storage. Check storage configuration."
                
        except Exception as e:
            logging.error(f"Error in MetaAgent.perform: {str(e)}")
            return f"Error generating agent: {str(e)}"
    
    def _generate_agent_code(self, class_name, description, parameters, agent_type):
        """
        Use Azure OpenAI to generate the agent code based on requirements.
        """
        if not self.client:
            logging.error("Azure OpenAI client not initialized")
            return None
        
        # Build the prompt based on agent type
        if agent_type == 'multi':
            example_code = self._get_multi_agent_example()
            agent_prompt = self._build_multi_agent_prompt(class_name, description, parameters)
        else:
            example_code = self._get_single_agent_example()
            agent_prompt = self._build_single_agent_prompt(class_name, description, parameters)
        
        try:
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert Python developer specializing in creating modular, reusable agent classes. "
                                   "Generate clean, well-documented code following Python best practices. "
                                   "IMPORTANT: Return ONLY the Python code without any markdown formatting, explanations, or code blocks. "
                                   "Do not include ```python or ``` markers."
                    },
                    {
                        "role": "user",
                        "content": agent_prompt
                    }
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            generated_code = response.choices[0].message.content.strip()
            
            # Remove markdown code blocks if present
            generated_code = self._clean_code_output(generated_code)
            
            return generated_code
            
        except Exception as e:
            logging.error(f"Error generating agent code with OpenAI: {str(e)}")
            return None
    
    def _build_single_agent_prompt(self, class_name, description, parameters):
        """Build the prompt for generating a single agent."""
        return f"""Create a Python agent class with the following specifications:

Class Name: {class_name}
Description: {description}
Parameters: {parameters if parameters else 'No specific parameters required'}

Requirements:
1. The class must inherit from BasicAgent
2. Implement __init__ with proper metadata including name, description, and parameters
3. Implement a perform(**kwargs) method that contains the agent's main logic
4. Include proper error handling and logging
5. Return meaningful success/error messages
6. Follow the pattern of the example agent below

Example pattern to follow:

{self._get_single_agent_example()}

Generate the complete agent class code now. Return ONLY the Python code without any markdown formatting."""
    
    def _build_multi_agent_prompt(self, class_name, description, parameters):
        """Build the prompt for generating a multi-agent."""
        return f"""Create a Python multi-agent orchestrator class with the following specifications:

Class Name: {class_name}
Description: {description}
Parameters: {parameters if parameters else 'Will coordinate multiple sub-agents'}

Requirements:
1. The class must inherit from BasicAgent
2. Accept a 'declared_agents' parameter in __init__ to access available agents
3. Implement logic to coordinate multiple agents based on the task
4. Include proper error handling and logging
5. Return consolidated results from multiple agent calls
6. Follow the pattern of the multi-agent example below

Example pattern to follow:

{self._get_multi_agent_example()}

Generate the complete multi-agent orchestrator class code now. Return ONLY the Python code without any markdown formatting."""
    
    def _get_single_agent_example(self):
        """Return an example of a simple single agent."""
        return """from agents.basic_agent import BasicAgent
import logging

class DataAnalysisAgent(BasicAgent):
    def __init__(self):
        self.name = 'DataAnalysis'
        self.metadata = {
            "name": self.name,
            "description": "Analyzes data and provides insights",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "string",
                        "description": "The data to analyze"
                    },
                    "analysis_type": {
                        "type": "string",
                        "description": "Type of analysis to perform"
                    }
                },
                "required": ["data"]
            }
        }
        super().__init__(name=self.name, metadata=self.metadata)
    
    def perform(self, **kwargs):
        data = kwargs.get('data')
        analysis_type = kwargs.get('analysis_type', 'basic')
        
        if not data:
            return "Error: No data provided for analysis"
        
        try:
            # Implement agent logic here
            result = f"Analyzed data with {analysis_type} analysis"
            logging.info(f"DataAnalysisAgent completed: {result}")
            return result
        except Exception as e:
            logging.error(f"Error in DataAnalysisAgent: {str(e)}")
            return f"Error: {str(e)}"
"""
    
    def _get_multi_agent_example(self):
        """Return an example of a multi-agent orchestrator."""
        return """from agents.basic_agent import BasicAgent
import logging

class ResearchOrchestratorAgent(BasicAgent):
    def __init__(self, declared_agents=None):
        self.name = 'ResearchOrchestrator'
        self.declared_agents = declared_agents or {}
        self.metadata = {
            "name": self.name,
            "description": "Orchestrates multiple agents to perform comprehensive research",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "The topic to research"
                    },
                    "depth": {
                        "type": "string",
                        "description": "Research depth: 'basic' or 'comprehensive'"
                    }
                },
                "required": ["topic"]
            }
        }
        super().__init__(name=self.name, metadata=self.metadata)
    
    def perform(self, **kwargs):
        topic = kwargs.get('topic')
        depth = kwargs.get('depth', 'basic')
        
        if not topic:
            return "Error: No topic provided for research"
        
        try:
            results = []
            
            # Example: Call multiple agents in sequence
            # Check if agents exist before calling
            if 'DataAnalysis' in self.declared_agents:
                agent = self.declared_agents['DataAnalysis']
                result = agent.perform(data=topic, analysis_type=depth)
                results.append(f"Analysis: {result}")
            
            # Consolidate results
            final_result = "Research Results:\\n" + "\\n".join(results)
            logging.info(f"ResearchOrchestrator completed for topic: {topic}")
            return final_result
            
        except Exception as e:
            logging.error(f"Error in ResearchOrchestrator: {str(e)}")
            return f"Error: {str(e)}"
"""
    
    def _clean_code_output(self, code):
        """Remove markdown code blocks and extra formatting from generated code."""
        # Remove ```python and ``` markers
        code = re.sub(r'^```python\s*\n', '', code, flags=re.MULTILINE)
        code = re.sub(r'^```\s*\n', '', code, flags=re.MULTILINE)
        code = re.sub(r'\n```\s*$', '', code, flags=re.MULTILINE)
        code = re.sub(r'^```\s*$', '', code, flags=re.MULTILINE)
        
        return code.strip()
    
    def _validate_agent_code(self, code):
        """
        Validate that the generated code contains required elements.
        Returns None if valid, or an error message if invalid.
        """
        if not code:
            return "Generated code is empty"
        
        # Check for required imports
        if 'from agents.basic_agent import BasicAgent' not in code:
            return "Missing required import: from agents.basic_agent import BasicAgent"
        
        # Check for class definition
        if 'class ' not in code or '(BasicAgent)' not in code:
            return "Missing class definition or BasicAgent inheritance"
        
        # Check for required methods
        if 'def __init__' not in code:
            return "Missing __init__ method"
        
        if 'def perform' not in code:
            return "Missing perform method"
        
        # Check for metadata
        if 'self.metadata' not in code:
            return "Missing metadata definition"
        
        # Try to compile the code (syntax check)
        try:
            compile(code, '<string>', 'exec')
        except SyntaxError as e:
            return f"Syntax error in generated code: {str(e)}"
        
        return None
    
    def _to_pascal_case(self, text):
        """Convert text to PascalCase for class names."""
        # Remove special characters and split on spaces/underscores
        words = re.sub(r'[^a-zA-Z0-9\s_]', '', text).split()
        # Capitalize each word and join
        return ''.join(word.capitalize() for word in words if word)
    
    def _to_snake_case(self, text):
        """Convert text to snake_case for file names."""
        # Remove special characters
        text = re.sub(r'[^a-zA-Z0-9\s_]', '', text)
        # Replace spaces with underscores and convert to lowercase
        text = re.sub(r'\s+', '_', text).lower()
        # Remove multiple underscores
        text = re.sub(r'_+', '_', text)
        return text.strip('_')
