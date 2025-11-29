from pathlib import Path
from src.Models.Models import CodeFile
class Lector:
    def __init__(self, ruta):
        self.ruta = Path(ruta).resolve()
        self.extensions = ["cpp", "java", "py"]

    def process(self, real_file : Path) -> CodeFile:
        file = real_file.relative_to(self.ruta)
        parts = list(file.parts)
        name = file.name.split('.')[0]
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
        return CodeFile(name, filename, real_file, extension, section, subsection)
    def list_code_files(self):
        code_files = []
        files = sorted(self.ruta.glob("**/*"))
        for real_file in files:
            ext = real_file.suffix[1:]
            if real_file.is_file() and ext in self.extensions:
                c = self.process(real_file)
                code_files.append(c)
        print(code_files)
        return code_files