from dataclasses import dataclass
from pathlib import Path

@dataclass
class CodeFile:
    title: str
    filename: str
    path: Path
    extension: str
    section: str
    subsection: str
    lexer: str