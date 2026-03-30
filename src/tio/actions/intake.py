import yaml
from pathlib import Path
from datetime import datetime
from rich.console import Console

console = Console()

class IntakeManager:
    """Manages the Academy intake process: starting, ingesting (via Bridge), and processing."""

    def __init__(self, orchestrator):
        self.tio = orchestrator
        self.root = Path("/srv/test.io")
        self.tmp_dir = self.root / "academy/tmp"
        self.state_file = self.root / ".agents/state/state.intake.yml"

    def _load_state(self):
        if not self.state_file.exists():
            return {"active": False, "inputs": []}
        with open(self.state_file, 'r') as f:
            return yaml.safe_load(f)

    def _save_state(self, state):
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.state_file, 'w') as f:
            yaml.dump(state, f)

    def start(self, title=None):
        """Initializes a new intake session."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        state = {
            "active": True,
            "session_id": f"intake_{timestamp}",
            "title": title or "New Academy Content",
            "start_time": datetime.now().isoformat(),
            "inputs": []
        }
        self._save_state(state)
        self.tio.log(f"Started new academy intake: [bold]{state['session_id']}[/bold]", "green")
        
        from .bridge import GeminiBridge
        bridge = GeminiBridge(self.tio)
        bridge.dispatch_intake_start(state['session_id'], state['title'])

    def ingest(self, content):
        """Adds raw content to session state and dispatches for Gemini to save."""
        state = self._load_state()
        if not state.get('active'):
            self.tio.log("Warning: No active intake session. Starting one now...", "yellow")
            self.start()
            state = self._load_state()

        if not content:
            self.tio.log("Error: No content provided for intake.", "red")
            return

        state['inputs'].append({
            "timestamp": datetime.now().isoformat(),
            "content": content
        })
        self._save_state(state)

        from .bridge import GeminiBridge
        bridge = GeminiBridge(self.tio)
        bridge.dispatch_intake_content(state['session_id'], content)

    def end(self):
        """Ends the intake session and triggers final synthesis."""
        state = self._load_state()
        if not state.get('active'):
            self.tio.log("Error: No active intake session to end.", "red")
            return

        state['active'] = False
        state['end_time'] = datetime.now().isoformat()
        self._save_state(state)

        from .bridge import GeminiBridge
        bridge = GeminiBridge(self.tio)
        bridge.dispatch_intake_end(state)
