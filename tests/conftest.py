"""Test fixtures for HiveCraft tests."""
import os
import shutil
import tempfile
import pytest
from pathlib import Path

@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    # Cleanup after test
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

@pytest.fixture
def valid_puzzle_dir(temp_dir):
    """Create a valid puzzle directory structure."""
    puzzle_dir = os.path.join(temp_dir, "valid_puzzle")
    os.makedirs(puzzle_dir, exist_ok=True)
    os.makedirs(os.path.join(puzzle_dir, "props"), exist_ok=True)
    
    # Create minimal valid files
    with open(os.path.join(puzzle_dir, "forge.py"), 'w') as f:
        f.write("""
import random
from typing import List

class Forge:
    def __init__(self, lines_count: int, unique_id: str):
        self.lines_count = lines_count
        self.unique_id = unique_id
        random.seed(unique_id)

    def run(self) -> List[str]:
        lines = []
        for i in range(self.lines_count):
            lines.append(self.generate_line(i))
        return lines
        
    def generate_line(self, index: int) -> str:
        return f"Line {index}: {random.randint(1, 100)}"
""")
            
    with open(os.path.join(puzzle_dir, "decrypt.py"), 'w') as f:
        f.write("""
from typing import List

class Decrypt:
    def __init__(self, lines: List[str]):
        self.lines = lines

    def run(self) -> str:
        return "42"
""")
            
    with open(os.path.join(puzzle_dir, "unveil.py"), 'w') as f:
        f.write("""
from typing import List

class Unveil:
    def __init__(self, lines: List[str]):
        self.lines = lines

    def run(self) -> str:
        return "24"
""")
            
    with open(os.path.join(puzzle_dir, "cipher.html"), 'w') as f:
        f.write("""<article>
  <h2>Test Cipher</h2>
  <p>This is a test cipher.</p>
</article>""")
            
    with open(os.path.join(puzzle_dir, "obscure.html"), 'w') as f:
        f.write("""<article>
  <h2>Test Obscure</h2>
  <p>This is a test obscure.</p>
</article>""")
    
    return puzzle_dir

@pytest.fixture
def invalid_puzzle_dir(temp_dir):
    """Create an invalid puzzle directory structure (missing files)."""
    puzzle_dir = os.path.join(temp_dir, "invalid_puzzle")
    os.makedirs(puzzle_dir, exist_ok=True)
    # No files, this makes it invalid
    return puzzle_dir

@pytest.fixture
def alghive_file(valid_puzzle_dir):
    """Create a temporary .alghive file for testing extract."""
    from hivecraft.alghive import Alghive
    alghive = Alghive(valid_puzzle_dir)
    alghive.zip_folder()
    alghive_path = f"{os.path.basename(valid_puzzle_dir)}.alghive"
    yield os.path.abspath(alghive_path)
    # Cleanup
    if os.path.exists(alghive_path):
        os.remove(alghive_path)
