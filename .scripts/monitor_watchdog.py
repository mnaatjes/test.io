#!/usr/bin/env python3
import time
import subprocess
import logging
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Project Constants
ROOT_DIR = Path("/srv/test.io")
AGENT_DIR = ROOT_DIR / ".agents"
LOG_FILE = AGENT_DIR / "logs" / "monitor_watchdog.log"
TIO_CLI = ROOT_DIR / ".scripts" / "tio-cli"

# Setup Logging
AGENT_DIR.joinpath("logs").mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class TioHandler(FileSystemEventHandler):
    """Listens for changes in .agents/ and triggers a sync."""
    
    def on_modified(self, event):
        if event.is_directory:
            return
        
        # Explicitly convert to string to satisfy the type checker
        src_path = str(event.src_path)
        
        # Only trigger for YAML files, and ignore the manifests themselves
        if src_path.endswith('.yml') and "manifests" not in src_path:
            logging.info(f"Change detected: {src_path}")
            self.trigger_sync()

    def trigger_sync(self):
        """Calls the tio-cli sync command."""
        try:
            # We use the full path to the tio-cli script
            subprocess.run([str(TIO_CLI), "sync"], check=True, capture_output=True)
            logging.info("Manifest sync triggered successfully.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Sync failed: {e.stderr.decode()}")

if __name__ == "__main__":
    event_handler = TioHandler()
    observer = Observer()
    observer.schedule(event_handler, str(AGENT_DIR), recursive=True)
    
    print(f"🟢 Watchdog started. Monitoring {AGENT_DIR}...")
    logging.info("Watchdog service started.")
    
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n🔴 Watchdog stopped.")
    observer.join()