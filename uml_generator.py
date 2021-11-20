
import io
import os
import sys

from constants import DEBUG_MODE, LOGGER, PLANTUMLS, UML_OPEN, UML_CLOSE


class UmlGenerator(object):

    def __init__(self, py_files: list[str]) -> None:
        self.py_files: list[str] = py_files
        self.classes: list = []
        self.class_relationships: dict = {}
        self.parents: dict = {}

    def get_package_name(self, index: int) -> str:
        "get_package_name()"
        # return the name of the .py file passed (omitting .py) as an argument to the argvs list to be used as the package name
        return os.path.basename(self.py_files[index].split('.')[0])

    def generate_plantuml_class_figure(self) -> None:
        "generate_plantuml_class_figure()"
        
        # by default, create a folder in the project directory to store the output .puml file
        if not os.path.exists(PLANTUMLS):
            os.makedirs(PLANTUMLS)

        # create a new .puml file to write to
        with open(f"{PLANTUMLS}/uml-garden.puml", 'w') as plantuml_file:

            # write out the conventional uml file header to the new .puml file created
            plantuml_file.write(f"{UML_OPEN}\n")

            # for each .py file passed to the program argvs list ...
            for py_file in self.py_files:

                # ... validate whether the argument passed is a file or folder name
                if '.' not in py_file:
                    sys.exit("folder argvs are unsupported")

                # ... capture the arguments index position in the argvs list
                index: int = self.py_files.index(py_file)

                if DEBUG_MODE:
                    LOGGER.debug(f"{self.write_pre_uml_content.__doc__}".replace("()", f"(plantuml_file=\"{plantuml_file.name}\", index={str(index)})"))

                # ... write out the .py package name to the new .puml file created
                self.write_pre_uml_content(plantuml_file, index)

            # write out the conventional uml file footer to the new .puml file created
            plantuml_file.write(f"{UML_CLOSE}\n")

    def write_pre_uml_content(self, plantuml_file: io.TextIOWrapper, index: int) -> None:
        "write_pre_uml_content()"

        if DEBUG_MODE:
            LOGGER.debug(f"{self.get_package_name.__doc__}".replace("()", f"(index={str(index)})"))
        
        # extract the name of the .py file passed (omitting .py) as an argument to the argvs list to be used as the package name
        package_name: str = self.get_package_name(index)

        self.class_name = None  # no type hinting recommended
        self.class_variables: dict = {}

        # write out the .py package name to the new .puml file created
        plantuml_file.write(f"package {package_name} {{\n")
