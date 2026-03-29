import yaml
import json
from pathlib import Path

class GeminiBridge:
    """Bridges the Python CLI to the Gemini CLI (The AI)."""

    def __init__(self, orchestrator):
        self.tio = orchestrator

    def dispatch_generator(self, module_name):
        """Prepares a directive for Gemini CLI based on a YAML generator."""
        if not module_name:
            self.tio.log("Error: Module name required for generation.", "red")
            return

        yml_path = self.tio.get_agent_path("generators", module_name, prefix="generator")
        
        if not yml_path:
            self.tio.log(f"Error: Generator for '{module_name}' not found.", "red")
            return

        with open(yml_path, 'r') as f:
            generator_data = yaml.safe_load(f)

        # The BRIDGE logic:
        # We output a structured directive that the Gemini CLI will recognize
        # If we're in 'raw' mode, we output just the instruction.
        # Otherwise, we wrap it for the user.
        
        directive_content = generator_data.get('generator', {}).get('description', 'No description found.')
        
        self.tio.log(f"Bridging to Gemini CLI for module: [bold]{module_name}[/bold]")
        
        # This is the "Magic String" that triggers you:
        instruction = (
            f"\n[DIRECTIVE: {module_name}]\n"
            f"Based on the following generator configuration:\n"
            f"{yaml.dump(generator_data)}\n"
            f"Please execute the 'state_generation' or 'manifest_sync' as defined."
        )
        
        # In a real shell, we might use `os.system(f"gemini '{instruction}'")`
        # But here, we print it so the user sees what the CLI is telling the AI.
        print(instruction)
