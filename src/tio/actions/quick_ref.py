import yaml
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

class QuickRefManager:
    """Handles ADHD-friendly cheat sheets and rules."""

    def __init__(self, orchestrator):
        self.tio = orchestrator

    def run(self, topic):
        if not topic:
            self.tio.log("Error: Topic required for Quick Ref (e.g., 'tio q academy')", "red")
            return

        # Handle 'academy[]' as 'academy'
        clean_topic = topic.replace("[]", "").replace('"', '').replace("'", "").replace("[", "").replace("]", "")
        
        yml_path = self.tio.get_agent_path("generators", clean_topic, prefix="generator.quick_reference")
        
        if not yml_path:
            yml_path = self.tio.get_agent_path("generators", clean_topic, prefix="generator")

        if not yml_path:
            self.tio.log(f"Error: Quick reference for '{clean_topic}' not found.", "red")
            return

        with open(yml_path, 'r') as f:
            data = yaml.safe_load(f)

        # Handle different YAML structures
        qr_data = data.get('quick_reference', {})
        summary = qr_data.get('cli_summary', [])
        
        if not summary:
            summary = [data.get('generator', {}).get('description', 'No summary available.')]

        panel_text = Text()
        for line in summary:
            if "!!" in line: panel_text.append(f"{line}\n", style="bold red")
            elif "->" in line: panel_text.append(f"{line}\n", style="green")
            elif "X " in line: panel_text.append(f"{line}\n", style="yellow")
            else: panel_text.append(f"• {line}\n", style="white")

        console.print(Panel(panel_text, title=f"[bold magenta]Quick Ref: {clean_topic.upper()}[/bold magenta]", expand=False))

        checks = qr_data.get('final_validation', [])
        if checks:
            console.print("\n[bold yellow]Final Validation Checklist:[/bold yellow]")
            for check in checks:
                console.print(f"  [cyan][ ][/cyan] {check}")
