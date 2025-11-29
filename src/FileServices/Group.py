from operator import attrgetter
from itertools import groupby
from pathlib import Path
from src.FileServices.Lector import Lector

class Group:
    def __init__(self, path: Path):
        self.hierarchy = []
        self.path = path
        self.build()
    def build(self):
        lector = Lector(self.path)
        codefiles = lector.list_code_files()
        codefiles.sort(key=attrgetter('section', 'subsection', 'title'))
        self.hierarchy = []
        for section_name, section_group in groupby(codefiles, key=attrgetter('section')):
            files_in_section = list(section_group)
            subsection_list = []
            for subsection_name, subsection_group in groupby(files_in_section, key=attrgetter('subsection')):
                files = list(subsection_group)
                subsection_list.append([subsection_name, files])
            self.hierarchy.append([section_name, subsection_list])