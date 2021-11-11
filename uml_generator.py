
import os
import sys

from constants import PLANTUMLS, UML_OPEN, UML_CLOSE


class UmlGenerator(object):

    def __init__(self, py_files: list[str]) -> None:
        self.py_files: list[str] = py_files

    def generate_plantuml_class_figure(self) -> None:
        # by default, create a folder in the project directory to store .puml files
        if not os.path.exists(PLANTUMLS):
            os.makedirs(PLANTUMLS)

        # create a new .puml file to write to
        with open(f"{PLANTUMLS}/uml-garden.puml", 'w') as plantuml_file:

            plantuml_file.write(f"{UML_OPEN}\n")

            # for each .py file passed to the program argvs list
            for py_file in self.py_files:
                # validate whether the argument passed is a file or folder
                if '.' not in py_file:
                    sys.exit("folder argvs are unsupported")

                # capture it's index position in the argvs list
                index: int = self.py_files.index(py_file)

            plantuml_file.write(f"{UML_CLOSE}\n")
