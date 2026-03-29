import yaml
import json
from pathlib import Path
from datetime import datetime
from rich.console import Console

console = Console()

class StateManager:
    """Manages the functional state of modules (Progress, Status, Locks)."""

    def __init__(self, orchestrator):
        self.tio = orchestrator
        self.state_dir = Path("/srv/test.io/.agents/state")

    def run(self, module):
        if not module:
            self.tio.log("Error: Module required for State (e.g., 'tio s academy')", "red")
            return

        if module == "*":
            self.tio.log("Listing all module states:")
            for s in self.state_dir.glob("state.*.yml"):
                self.show_state(s.stem.split('.')[-1])
            return

        self.show_state(module)

    def show_state(self, module):
        state_file = self.state_dir / f"state.{module}.yml"
        if not state_file.exists():
            self.tio.log(f"No state found for '{module}'. Generating initialized state...", "yellow")
            self.init_state(module)
            return

        with open(state_file, 'r') as f:
            data = yaml.safe_load(f)

        status_color = "green" if data.get('status') == 'updated' else "yellow"
        lock_icon = "[red]LOCKED[/red]" if data.get('locked') else "[green]OPEN[/green]"
        
        self.tio.log(f"Module: [bold]{module}[/bold] | Status: [{status_color}]{data.get('status')}[/{status_color}] | {lock_icon}")
        
    def init_state(self, module):
        # We can use the generator bridge here or just write a basic one
        from .bridge import GeminiBridge
        bridge = GeminiBridge(self.tio)
        bridge.dispatch_generator("state")
