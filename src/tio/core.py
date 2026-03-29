import os
import yaml
import json
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

ROOT_DIR = Path("/srv/test.io")
AGENT_DIR = ROOT_DIR / ".agents"
console = Console()

class TioOrchestrator:
    """Core logic for managing directives and triggering Gemimi."""
    
    SHORTHANDS = {
        "g": ("generate", "Run a generator (Calls Gemini for AI reasoning)"),
        "s": ("state", "Manage module state and progress tracking"),
        "m": ("monitor", "Activate/Deactivate background monitors"),
        "sync": ("sync", "Synchronize all JSON manifests (Enhanced Discovery)"),
        "d": ("discovery", "Ingest project structure/files (Token Efficient)"),
        "q": ("quick_ref", "Show ADHD-friendly cheat sheets and rules"),
        "z": ("quiz", "Manage Academy quizzes and get AI-assisted answers"),
        "l": ("list", "Show command registry table"),
        "h": ("help", "Display all available commands and what they do")
    }

    VERBOSE_HELP = {
        "z": {
            "title": "Quiz Action (z / quiz)",
            "details": "Manages Academy quizzes. Use --start to begin, input questions for AI help, and --eoq to finish.",
            "params": "<question_text> or flags (--start, --eoq)",
            "yaml_interaction": "Uses .agents/state/state.quiz.yml and stores in academy/quizzes/",
            "example": "tio z --start 'Module 2'"
        },
        "m": {
            "title": "Monitor Action (m / monitor)",
            "details": "Manages background monitor status. Can start, stop, or check status.",
            "params": "<module_name> or '*' (all monitors)",
            "yaml_interaction": "Updates .agents/monitors/monitor.{module}.yml",
            "example": "tio m academy --stop"
        }
    }

    def __init__(self, raw_mode=False, options=None):
        self.raw_mode = raw_mode
        self.options = options or {}

    def log(self, message, style="cyan"):
        if not self.raw_mode:
            console.print(f"[{style}]>[/{style}] {message}")

    def show_usage(self, verbose=False, target=None):
        """Displays command registry or deep-dive help."""
        if verbose and target and target in self.VERBOSE_HELP:
            info = self.VERBOSE_HELP[target]
            panel_content = Text.from_markup(
                f"[bold cyan]Action:[/bold cyan] {info['title']}\n"
                f"[bold cyan]Detail:[/bold cyan] {info['details']}\n"
                f"[bold cyan]Params:[/bold cyan] [green]{info['params']}[/green]\n"
                f"[bold cyan]YAML:[/bold cyan]   [yellow]{info['yaml_interaction']}[/yellow]\n"
                f"[bold cyan]Usage:[/bold cyan]  [white]{info['example']}[/white]"
            )
            console.print(Panel(panel_content, title=f"Deep Dive: {target}", expand=False))
            return

        table = Table(title="[bold cyan]Tio-CLI Command Registry[/bold cyan]", show_header=True, header_style="bold magenta")
        table.add_column("Short", style="dim", width=6, justify="center")
        table.add_column("Command", style="green")
        table.add_column("Description")
        for short, (full, desc) in self.SHORTHANDS.items():
            table.add_row(short, full, desc)
        console.print(table)

    def execute(self, cmd, module=None):
        """Dispatches commands to specific action modules."""
        if cmd == "sync":
            from .actions.sync import SyncManager
            SyncManager(self).run()
            return

        if cmd in ["q", "quick_ref"]:
            from .actions.quick_ref import QuickRefManager
            QuickRefManager(self).run(module)
            return

        if cmd in ["z", "quiz"]:
            from .actions.quiz import QuizManager
            manager = QuizManager(self)
            if self.options.get("quiz_start"):
                manager.start(self.options.get("quiz_start"))
            elif self.options.get("quiz_end"):
                manager.end()
            else:
                manager.answer(module)
            return

        if cmd in ["m", "monitor"]:
            from .actions.monitor import MonitorManager
            # Pass options to the manager
            MonitorManager(self).run(module, stop=self.options.get("stop"), start=self.options.get("start"))
            return

        if cmd in ["s", "state"]:
            from .actions.state import StateManager
            StateManager(self).run(module)
            return

        if cmd in ["n", "notes"]:
            from .actions.notes import NotesManager
            NotesManager(self).run(module)
            return

        if cmd in ["d", "discovery"]:
            from .actions.discovery import DiscoveryManager
            disco = DiscoveryManager(ROOT_DIR)
            results = disco.read_folder(module or ".")
            if self.raw_mode:
                print(json.dumps(results, indent=2))
            else:
                self.log(f"Discovery found {len(results)} files in '{module or '.'}'")
            return

        if cmd in ["g", "generate"]:
            from .actions.bridge import GeminiBridge
            GeminiBridge(self).dispatch_generator(module)
            return

    def get_agent_path(self, sub_dir, module_name, prefix="generator"):
        target = AGENT_DIR / sub_dir / f"{prefix}.{module_name}.yml"
        if not target.exists():
            return None
        return target
