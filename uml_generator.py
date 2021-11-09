
import os

from constants import PLANTUMLS, UML_OPEN, UML_CLOSE


class UmlGenerator(object):

    def __init__(self, py_files: list[str]) -> None:
        self.py_files: list[str] = py_files

    def generate_plantuml_class_figure(self) -> None:
        if not os.path.exists(PLANTUMLS):
            os.makedirs(PLANTUMLS)

        with open(f"{PLANTUMLS}/uml-garden.puml", 'w') as plantuml_file:
            plantuml_file.write(f"{UML_OPEN}\n")
            plantuml_file.write(f"{UML_CLOSE}\n")
