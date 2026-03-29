import json
import pytest
from src.tio.actions.sync import SyncManager
from src.tio.core import TioOrchestrator
from pathlib import Path

def test_sync_manager_run(tmp_path):
    # Setup temporary .agents structure
    agent_dir = tmp_path / ".agents"
    (agent_dir / "generators").mkdir(parents=True)
    (agent_dir / "manifests").mkdir(parents=True)
    
    # Create dummy generator
    (agent_dir / "generators" / "generator.test.yml").write_text("locked: false\nid: test")
    
    # Mock orchestrator
    class MockOrchestrator:
        def __init__(self): self.raw_mode = True
        def log(self, msg, style=""): pass

    sync = SyncManager(MockOrchestrator())
    sync.root = tmp_path
    sync.agent_dir = agent_dir
    sync.manifest_dir = agent_dir / "manifests"
    sync.discovery.root = tmp_path
    
    sync.run()
    
    # Check if manifest was created
    manifest_file = agent_dir / "manifests" / "manifest.generators.json"
    assert manifest_file.exists()
    
    with open(manifest_file, 'r') as f:
        data = json.load(f)
        assert data["directory"] == "generators"
        assert len(data["files"]) == 1
        assert data["files"][0]["id"] == "test"
