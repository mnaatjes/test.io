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
        "l": ("list", "Show command registry table"),
        "h": ("help", "Display all available commands and what they do")
    }

    VERBOSE_HELP = {
        "g": {
            "title": "Generator Action (g / generate)",
            "details": "Triggers an AI-driven transformation. It reads a YAML file in .agents/generators/ and sends it to the Gemini CLI as a directive.",
            "params": "<module_name> (e.g., 'state', 'bugs', 'notes')",
            "yaml_interaction": "Uses generator.{module}.yml",
            "example": "tio g academy"
        },
        "sync": {
            "title": "Sync Action (sync)",
            "details": "Rebuilds all system manifests and performs a full workspace discovery scan.",
            "params": "None",
            "yaml_interaction": "Scans all .yml files; checks for 'locked: true' property.",
            "example": "tio sync"
        },
        "d": {
            "title": "Discovery Action (d / discovery)",
            "details": "Performs a token-efficient scan of the project structure to build a machine-readable map.",
            "params": "<directory_path> (defaults to project root '.')",
            "yaml_interaction": "Respects .gitignore patterns.",
            "example": "tio d academy/notes"
        },
        "s": {
            "title": "State Action (s / state)",
            "details": "Updates or reads the functional state of a module. Tracks progress and versioning.",
            "params": "<module_name> (e.g., 'academy')",
            "yaml_interaction": "Modifies .agents/state/state.{module}.yml",
            "example": "tio s academy"
        }
    }

    def __init__(self, raw_mode=False):
        self.raw_mode = raw_mode

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
        
        usage_text = Text.from_markup(
            "\n[bold yellow]Usage:[/bold yellow] [green]tio <command> <module>[/green]\n"
            "[bold yellow]Detailed Help:[/bold yellow] [white]tio h <cmd>[/white] (e.g., [dim]tio h g[/dim])"
        )
        console.print(usage_text)

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

        if cmd in ["d", "discovery"]:
            from .actions.discovery import DiscoveryManager
            disco = DiscoveryManager(ROOT_DIR)
            results = disco.read_folder(module or ".")
            if self.raw_mode:
                print(json.dumps(results, indent=2))
            else:
                self.log(f"Discovery found {len(results)} files in '{module or '.'}'")
                for r in results[:10]:
                    print(f"  - {r['rel_path']} ({r['size']} bytes)")
                if len(results) > 10:
                    print(f"  ... and {len(results)-10} more.")
            return

        if cmd in ["g", "generate"]:
            from .actions.bridge import GeminiBridge
            GeminiBridge(self).dispatch_generator(module)
            return

        if cmd in ["l", "list"]:
            self.show_usage()
        else:
            self.log(f"Command '{cmd}' not implemented yet or unknown.", style="red")

    def get_agent_path(self, sub_dir, module_name, prefix="generator"):
        target = AGENT_DIR / sub_dir / f"{prefix}.{module_name}.yml"
        if not target.exists():
            return None
        return target
