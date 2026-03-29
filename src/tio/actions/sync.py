import json
from datetime import datetime
from pathlib import Path
import yaml
from .discovery import DiscoveryManager

class SyncManager:
    """Handles the deterministic JSON manifest synchronization with enhanced discovery."""

    def __init__(self, orchestrator):
        self.tio = orchestrator
        self.root = Path("/srv/test.io")
        self.agent_dir = self.root / ".agents"
        self.manifest_dir = self.agent_dir / "manifests"
        self.discovery = DiscoveryManager(self.root)

    def run(self):
        self.tio.log("Starting enhanced manifest synchronization...")
        self.manifest_dir.mkdir(parents=True, exist_ok=True)
        
        # 1. Individual module manifests
        directories = ["generators", "monitors", "state", "templates"]
        for dir_name in directories:
            target_path = self.agent_dir / dir_name
            if not target_path.exists():
                continue

            manifest_data = {
                "directory": dir_name,
                "last_sync": datetime.now().isoformat(),
                "files": []
            }

            for yml_file in target_path.glob("*.yml"):
                locked = self.check_lock(yml_file)
                manifest_data["files"].append({
                    "id": yml_file.stem.split('.')[-1],
                    "path": str(yml_file.relative_to(self.root)),
                    "locked": locked,
                    "size": yml_file.stat().st_size
                })

            output_file = self.manifest_dir / f"manifest.{dir_name}.json"
            with open(output_file, 'w') as f:
                json.dump(manifest_data, f, indent=2)
            self.tio.log(f"Synced {dir_name} -> {output_file.name}", style="green")

        # 2. Global Workspace Snapshot (The "Discovery" Manifest)
        workspace_map = self.discovery.read_folder(".", recursive=True)
        workspace_manifest = {
            "type": "project-snapshot",
            "last_sync": datetime.now().isoformat(),
            "file_count": len(workspace_map),
            "files": workspace_map
        }
        
        workspace_file = self.manifest_dir / "manifest.workspace.json"
        with open(workspace_file, 'w') as f:
            json.dump(workspace_manifest, f, indent=2)
        self.tio.log(f"Synced workspace -> {workspace_file.name} (Files indexed: {len(workspace_map)})", style="green")

    def check_lock(self, yml_path):
        try:
            with open(yml_path, 'r') as f:
                data = yaml.safe_load(f)
                return data.get('locked', False) if data else False
        except Exception:
            return False
