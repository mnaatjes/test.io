#!/usr/bin/env python3
"""
Author: Michael Naatjes (via Gemini CLI)
Date: 2024-03-29
Description: Deterministic manifest synchronization for the TestIO Agent ecosystem.
Dependencies: PyYAML, pathlib
"""

import os
import sys
import json
import yaml
from datetime import datetime
from pathlib import Path

# Configuration
ROOT_DIR = Path("/srv/test.io")
AGENT_DIR = ROOT_DIR / ".agents"
MANIFEST_DIR = AGENT_DIR / "manifests"
TARGET_DIRS = ["generators", "monitors", "state", "templates"]

def check_lock(yml_path):
    """Checks for 'locked: true' in a YAML file."""
    try:
        with open(yml_path, 'r') as f:
            data = yaml.safe_load(f)
            return data.get('locked', False) if data else False
    except Exception as e:
        print(f"  [!] Error reading {yml_path.name}: {e}")
        return False

def sync_manifests():
    """Scans directories and synchronizes JSON manifests."""
    print(f">>> Initializing Manifest Sync [ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ]")
    
    if not MANIFEST_DIR.exists():
        MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
        print(f"  [+] Created manifest directory: {MANIFEST_DIR}")

    for dir_name in TARGET_DIRS:
        target_path = AGENT_DIR / dir_name
        if not target_path.exists():
            print(f"  [-] Skipping {dir_name}: Directory not found.")
            continue

        manifest_data = {
            "directory": dir_name,
            "last_sync": datetime.now().isoformat(),
            "environment": "Debian 13 / i3wm",
            "files": []
        }

        # Find all .yml files in the target directory
        for yml_file in target_path.glob("*.yml"):
            locked = check_lock(yml_file)
            manifest_data["files"].append({
                "id": yml_file.stem.split('.')[-1],
                "filename": yml_file.name,
                "path": str(yml_file.relative_to(ROOT_DIR)),
                "locked": locked
            })

        output_file = MANIFEST_DIR / f"manifest.{dir_name}.json"
        try:
            with open(output_file, 'w') as f:
                json.dump(manifest_data, f, indent=2)
            print(f"  [✔] {dir_name.capitalize()} -> {output_file.name} (Count: {len(manifest_data['files'])})")
        except Exception as e:
            print(f"  [✘] Failed to write {output_file.name}: {e}")

if __name__ == "__main__":
    try:
        sync_manifests()
        print(">>> Sync Complete.")
    except KeyboardInterrupt:
        print("\n[!] Sync aborted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n[CRITICAL ERROR]: {e}")
        sys.exit(1)
