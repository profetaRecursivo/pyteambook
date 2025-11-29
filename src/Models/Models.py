from dataclasses import dataclass
from pathlib import Path
from typing import List

@dataclass
class CodeFile:
    title: str
    filename: str
    path: Path
    extension: str
    section: str
    subsection: str