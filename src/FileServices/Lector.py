from pathlib import Path
from src.Models.Models import CodeFile


class Lector:
    def __init__(self, path):
        self.path = Path(path).resolve()
        if not self.path.exists():
            raise FileNotFoundError(f"Directory not found: {self.path}")
        if not self.path.is_dir():
            raise NotADirectoryError(f"Path is not a directory: {self.path}")
        self.extensions = ["cpp", "java", "py"]

    def latex_escape(self, text: str) -> str:
        return (
            text.replace("_", r"\_")
            .replace("#", r"\#")
            .replace("&", r"\&")
            .replace("%", r"\%")
        )

    def process(self, real_file: Path) -> CodeFile:
        file = real_file.relative_to(self.path)
        parts = list(file.parts)
        name = file.name.split(".")[0]
        extension = file.suffix[1:]
        section = "General"
        subsection = "General"
        if len(parts) == 1:
            filename = parts[0]
        elif len(parts) == 2:
            section = parts[0]
            filename = parts[1]
        elif len(parts) == 3:
            section = parts[0]
            subsection = parts[1]
            filename = parts[2]
        else:
            section = parts[0]
            subsection = parts[1]
            filename = " ".join(parts[2:])

        name = self.latex_escape(name)
        filename = self.latex_escape(filename)
        section = self.latex_escape(section)
        subsection = self.latex_escape(subsection)

        lexer_map = {
            "cpp": "cpp",
            "cc": "cpp",
            "cxx": "cpp",
            "h": "cpp",
            "hpp": "cpp",
            "py": "python",
            "py3": "python",
            "java": "java",
            "sh": "bash",
            "bash": "bash",
        }
        lexer = lexer_map.get(extension, "text")

        codefile = CodeFile(name, filename, real_file, extension, section, subsection, lexer)
        return codefile

    def list_code_files(self):
        code_files = []
        files = sorted(self.path.glob("**/*"))
        for real_file in files:
            ext = real_file.suffix[1:]
            if real_file.is_file() and ext in self.extensions:
                c = self.process(real_file)
                code_files.append(c)
        return code_files