import os
import fnmatch
from pathlib import Path
import yaml

class DiscoveryManager:
    """Optimized discovery and ingestion methods to reduce AI cycles/tokens."""

    def __init__(self, root_dir="/srv/test.io"):
        self.root = Path(root_dir)
        self.ignore_patterns = self._load_ignore_patterns()

    def _load_ignore_patterns(self):
        """Loads patterns from .gitignore and adds standard defaults."""
        patterns = [".git/", ".venv/", "__pycache__/", "*.pyc", ".agents/manifests/"]
        gitignore = self.root / ".gitignore"
        if gitignore.exists():
            with open(gitignore, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        patterns.append(line)
        return patterns

    def is_ignored(self, path):
        """Checks if a path matches any ignore patterns."""
        rel_path = str(Path(path).relative_to(self.root))
        for pattern in self.ignore_patterns:
            if fnmatch.fnmatch(rel_path, pattern) or fnmatch.fnmatch(rel_path.split('/')[0] + "/", pattern):
                return True
        return False

    def read_folder(self, sub_dir=".", recursive=True):
        """ReadFolder: Recursive scan of a directory, returning a flat list of metadata."""
        target = self.root / sub_dir
        results = []
        
        search_pattern = "**/*" if recursive else "*"
        for p in target.glob(search_pattern):
            if p.is_file() and not self.is_ignored(p):
                results.append({
                    "name": p.name,
                    "rel_path": str(p.relative_to(self.root)),
                    "size": p.stat().st_size,
                    "mtime": p.stat().st_mtime,
                    "ext": p.suffix
                })
        return results

    def find_file(self, pattern):
        """FindFile: Search for files across the project matching a glob pattern."""
        return [str(p.relative_to(self.root)) for p in self.root.glob(f"**/{pattern}") if not self.is_ignored(p)]

    def read_file_optimized(self, file_path, max_lines=None):
        """ReadFile: Reads a file. If max_lines is set, it reads head and tail to save tokens."""
        full_path = self.root / file_path
        if not full_path.exists():
            return None
        
        with open(full_path, 'r') as f:
            lines = f.readlines()
            
        if max_lines and len(lines) > max_lines:
            half = max_lines // 2
            content = "".join(lines[:half]) + "\n... [TRUNCATED] ...\n" + "".join(lines[-half:])
            return content
        return "".join(lines)
