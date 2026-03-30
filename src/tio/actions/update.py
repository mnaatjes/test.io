import json
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from .sync import SyncManager

class UpdateManager:
    """Action for re-initializing and updating the Gemini context with the latest project data."""

    def __init__(self, orchestrator):
        self.tio = orchestrator
        self.root = Path("/srv/test.io")
        self.manifest_dir = self.root / ".agents" / "manifests"
        self.console = Console()

    def run(self):
        # 1. First, synchronize everything
        sync_manager = SyncManager(self.tio)
        sync_manager.run()
        
        # 2. Collect manifest summaries
        summary = self.get_summary()
        
        # 3. Present the status report
        self.display_report(summary)

    def get_summary(self):
        summary = {
            "timestamp": datetime.now().isoformat(),
            "manifests": {}
        }
        
        for manifest_file in self.manifest_dir.glob("manifest.*.json"):
            try:
                with open(manifest_file, 'r') as f:
                    data = json.load(f)
                    summary["manifests"][manifest_file.stem.replace("manifest.", "")] = data
            except Exception as e:
                self.tio.log(f"Error reading manifest {manifest_file}: {e}", style="red")
        
        return summary

    def display_report(self, summary):
        self.tio.log("Gemini Context Updated Successfully", style="bold green")
        
        # Global Snapshot
        workspace = summary["manifests"].get("workspace", {})
        ws_panel = Panel(
            Text.from_markup(
                f"[bold cyan]Last Sync:[/bold cyan] {workspace.get('last_sync', 'N/A')}\n"
                f"[bold cyan]File Count:[/bold cyan] {workspace.get('file_count', 0)}\n"
                f"[bold cyan]Root Path:[/bold cyan] {self.root}"
            ),
            title="Workspace Snapshot",
            expand=False
        )
        self.console.print(ws_panel)

        # Module State
        state_data = summary["manifests"].get("state", {})
        if state_data:
            state_table = Table(title="Module Status", show_header=True, header_style="bold magenta")
            state_table.add_column("Module ID", style="cyan")
            state_table.add_column("Path", style="dim")
            state_table.add_column("Locked", justify="center")
            
            for f in state_data.get("files", []):
                locked = "[red]Yes[/red]" if f.get("locked") else "[green]No[/green]"
                state_table.add_row(f.get("id"), f.get("path"), locked)
            self.console.print(state_table)

        # Active Monitors
        monitor_data = summary["manifests"].get("monitors", {})
        if monitor_data:
            monitor_list = [f.get("id") for f in monitor_data.get("files", [])]
            self.tio.log(f"Available Monitors: {', '.join(monitor_list)}", style="yellow")

        # Generators
        gen_data = summary["manifests"].get("generators", {})
        if gen_data:
            gen_count = len(gen_data.get("files", []))
            self.tio.log(f"Registered Generators: {gen_count} (use 'tio g <id>' to trigger)", style="green")

        # Main configuration check
        main_yml = self.root / ".agents" / "main.yml"
        if main_yml.exists():
            self.tio.log(f"Configuration loaded from {main_yml.relative_to(self.root)}", style="blue")
