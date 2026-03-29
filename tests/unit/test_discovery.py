import pytest
from src.tio.actions.discovery import DiscoveryManager
from pathlib import Path

def test_discovery_read_folder(tmp_path):
    # Create a dummy structure
    (tmp_path / "file1.txt").write_text("content1")
    (tmp_path / "subdir").mkdir()
    (tmp_path / "subdir" / "file2.txt").write_text("content2")
    
    # Discovery instance pointed at tmp_path
    disco = DiscoveryManager(root_dir=tmp_path)
    results = disco.read_folder(".")
    
    # We expect 2 files
    assert len(results) == 2
    paths = [r['rel_path'] for r in results]
    assert "file1.txt" in paths
    assert "subdir/file2.txt" in paths

def test_discovery_find_file(tmp_path):
    (tmp_path / "target.yml").write_text("content")
    disco = DiscoveryManager(root_dir=tmp_path)
    results = disco.find_file("target.yml")
    assert "target.yml" in results

def test_discovery_read_file_optimized(tmp_path):
    f = tmp_path / "long.txt"
    f.write_text("\n".join([f"line {i}" for i in range(20)]))
    
    disco = DiscoveryManager(root_dir=tmp_path)
    # Test head/tail truncation
    content = disco.read_file_optimized("long.txt", max_lines=10)
    assert "[TRUNCATED]" in content
    assert "line 0" in content
    assert "line 19" in content
