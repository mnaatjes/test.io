import yaml
from pathlib import Path
from rich.console import Console

console = Console()

class MonitorManager:
    """Manages background monitors (Status checks, Activation, Deactivation)."""

    def __init__(self, orchestrator):
        self.tio = orchestrator
        self.monitor_dir = Path("/srv/test.io/.agents/monitors")

    def run(self, module, stop=False, start=False):
        if not module or module == "*":
            self.tio.log("Executing batch monitor operation...")
            for m in self.monitor_dir.glob("monitor.*.yml"):
                self.show_monitor(m.stem.split('.')[-1], stop, start)
            return

        self.show_monitor(module, stop, start)

    def show_monitor(self, module, stop=False, start=False):
        monitor_file = self.monitor_dir / f"monitor.{module}.yml"
        if not monitor_file.exists():
            self.tio.log(f"No monitor found for '{module}'.", "yellow")
            return

        with open(monitor_file, 'r') as f:
            data = yaml.safe_load(f)

        if stop:
            data['status'] = 'paused'
            with open(monitor_file, 'w') as f:
                yaml.dump(data, f)
            self.tio.log(f"Monitor: [bold]{module}[/bold] | Status: [yellow]PAUSED[/yellow]", style="green")
        elif start:
            data['status'] = 'active'
            with open(monitor_file, 'w') as f:
                yaml.dump(data, f)
            self.tio.log(f"Monitor: [bold]{module}[/bold] | Status: [green]ACTIVE[/green]", style="green")
        else:
            status_color = "green" if data.get('status') == 'active' else "yellow"
            self.tio.log(f"Monitor: [bold]{module}[/bold] | Status: [{status_color}]{data.get('status')}[/{status_color}] | Watch: {data.get('watch_path')}")
