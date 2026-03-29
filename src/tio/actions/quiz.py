import yaml
import json
from pathlib import Path
from datetime import datetime
from rich.console import Console

console = Console()

class QuizManager:
    """Manages the quiz process: starting, answering (via Bridge), and ending."""

    def __init__(self, orchestrator):
        self.tio = orchestrator
        self.root = Path("/srv/test.io")
        self.question_dir = self.root / "academy/quizzes/questions"
        self.notes_dir = self.root / "academy/quizzes/notes"
        self.state_file = self.root / ".agents/state/state.quiz.yml"

    def _load_state(self):
        if not self.state_file.exists():
            return {"active": False, "questions": []}
        with open(self.state_file, 'r') as f:
            return yaml.safe_load(f)

    def _save_state(self, state):
        with open(self.state_file, 'w') as f:
            yaml.dump(state, f)

    def start(self, quiz_number=None):
        """Initializes a new quiz session."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        state = {
            "active": True,
            "quiz_id": f"quiz_{quiz_number or timestamp}",
            "start_time": datetime.now().isoformat(),
            "questions": []
        }
        self._save_state(state)
        self.tio.log(f"Started new quiz: [bold]{state['quiz_id']}[/bold]", "green")

    def end(self, reason="completed"):
        """Ends the quiz session and prompts for the outcome."""
        state = self._load_state()
        if not state.get('active'):
            self.tio.log("Error: No active quiz session to end.", "red")
            return

        state['active'] = False
        state['end_time'] = datetime.now().isoformat()
        self._save_state(state)

        # This triggers a Bridge call so Gemini can ask for the outcome and write the report
        from .bridge import GeminiBridge
        bridge = GeminiBridge(self.tio)
        bridge.dispatch_quiz_end(state, reason)

    def answer(self, question_text):
        """Prepares a directive for Gemini to answer the question using notes/refs."""
        state = self._load_state()
        if not state.get('active'):
            self.tio.log("Warning: No active quiz session. Starting one now...", "yellow")
            self.start()
            state = self._load_state()

        # Build the context: Find all relevant notes and refs
        # We'll use the discovery manifest for this
        manifest_path = self.root / ".agents/manifests/manifest.workspace.json"
        context_files = []
        if manifest_path.exists():
            with open(manifest_path, 'r') as f:
                manifest = json.load(f)
                for f_info in manifest.get('files', []):
                    path = f_info['rel_path']
                    if path.startswith("academy/notes/") or "generator.quick_reference" in path:
                        context_files.append(path)

        # Trigger the Bridge
        from .bridge import GeminiBridge
        bridge = GeminiBridge(self.tio)
        bridge.dispatch_quiz_question(question_text, context_files, state['quiz_id'])
