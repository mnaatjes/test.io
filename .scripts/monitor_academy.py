#!/usr/bin/env python3
"""
Author: Michael Naatjes (via Gemini CLI)
Date: 2024-03-29
Description: Event-driven monitor for the 'academy' module.
Dependencies: watchdog, PyYAML
"""

import time
import os
import sys
import yaml
import subprocess
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuration
WATCH_DIR = Path("/srv/test.io/academy/notes/")
STATE_FILE = Path("/srv/test.io/.agents/state/state.academy.yml")
MONITOR_CONFIG = Path("/srv/test.io/.agents/monitors/monitor.academy.yml")

class AcademyMonitorHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_trigger = 0
        self.debounce_ms = 1000  # Default debounce

    def is_locked(self):
        """Checks if the state is manually locked."""
        if not STATE_FILE.exists():
            return False
        try:
            with open(STATE_FILE, 'r') as f:
                data = yaml.safe_load(f)
                return data.get('locked', False) if data else False
        except Exception as e:
            print(f"  [!] Monitor Error reading state lock: {e}")
            return True # Fail-safe to locked

    def on_modified(self, event):
        if event.is_directory:
            return
        
        # Debounce to prevent multiple triggers for a single save
        current_time = time.time() * 1000
        if current_time - self.last_trigger < self.debounce_ms:
            return
        self.last_trigger = current_time

        print(f">>> Change detected in: {event.src_path}")
        
        if self.is_locked():
            print("  [!] State is LOCKED. Skipping automated trigger.")
            return

        print(f"  [>] Triggering: ./bin/tio g notes")
        try:
            # We run the command via subprocess
            subprocess.run(["/srv/test.io/bin/tio", "g", "notes"], check=True)
            print("  [✔] Trigger successful.")
        except Exception as e:
            print(f"  [✘] Trigger failed: {e}")

def main():
    if not WATCH_DIR.exists():
        WATCH_DIR.mkdir(parents=True, exist_ok=True)
        print(f"  [+] Created watch directory: {WATCH_DIR}")

    print(f">>> Starting Academy Monitor on {WATCH_DIR}")
    print(f">>> Lock check: {STATE_FILE}")
    
    event_handler = AcademyMonitorHandler()
    observer = Observer()
    observer.schedule(event_handler, str(WATCH_DIR), recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n[!] Monitor stopped by user.")
    observer.join()

if __name__ == "__main__":
    main()
