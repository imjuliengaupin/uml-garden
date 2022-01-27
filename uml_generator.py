
import io
import os
import re as regex
import sys

from constants import PLANTUMLS, UML_OPEN, UML_CLOSE


class UmlGenerator(object):

    def __init__(self, py_files: list[str]) -> None:
        self.py_files: list[str] = py_files
        self.classes: list = []
        self.class_relationships: dict = {}
        self.parents: dict = {}

        self.is_newline_found: regex.Pattern = regex.compile(r"^\s*(:?$|#|raise|print)")
        self.is_base_class_found: regex.Pattern = regex.compile(r"^class\s+([\w\d]+)\(\)\s*:")

    def get_package_name(self, index: int) -> str:
        # return the name of the .py file passed (omitting .py) as an argument to the argvs list to be used as the package name
        return os.path.basename(self.py_files[index].split('.')[0])

    def generate_plantuml_class_figure(self) -> None:
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

                # ... write out the .py package name to the new .puml file created
                self.write_pre_uml_content(plantuml_file, index)

                # TEST for commenting purposes to determine the representation of self.class_variables in uml diagram
                self.write_core_uml_content(plantuml_file, py_file)

                # TEST for commenting purposes to determine the representation of self.class_variables in uml diagram
                self.write_post_uml_content(plantuml_file)

            # TEST for commenting purposes to determine the representation of self.class_variables in uml diagram
            self.write_post_uml_relationship_content(plantuml_file)

            # write out the conventional uml file footer to the new .puml file created
            plantuml_file.write(f"{UML_CLOSE}\n")
    
    def set_class_name_uml_notation(self, plantuml_file: io.TextIOWrapper, base_or_child_class_name: str, parent_class_name: str) -> None:
        pass

    def write_pre_uml_content(self, plantuml_file: io.TextIOWrapper, index: int) -> None:
        # extract the name of the .py file passed (omitting .py) as an argument to the argvs list to be used as the package name
        package_name: str = self.get_package_name(index)

        self.class_name = None  # no type hinting recommended
        self.class_variables: dict = {}

        # write out the .py package name to the new .puml file created
        plantuml_file.write(f"package {package_name} {{\n")

    def write_core_uml_content(self, plantuml_file: io.TextIOWrapper, py_file: str) -> None:

        for line_of_code in open(py_file, 'r'):
            # if a newline "\n" is found in the code file being read, ignore it
            if self.is_newline_found.match(line_of_code):
                continue

            base_class_found = self.is_base_class_found.match(line_of_code)

            if base_class_found:
                base_class_name = base_class_found.group(1)

                self.set_class_name_uml_notation(plantuml_file, base_class_name, "")

                continue

    def write_post_uml_content(self, plantuml_file: io.TextIOWrapper) -> None:

        for class_name, class_members in self.class_variables.items():
            for class_member in class_members:
                plantuml_file.write(f"{class_name} : {class_member}\n")

        plantuml_file.write("}\n\n")

    def write_post_uml_relationship_content(self, plantuml_file: io.TextIOWrapper) -> None:

        for child_class, parent_class in self.parents.items():
            if not parent_class or parent_class == "object":
                continue
            plantuml_file.write(f"{parent_class} <|-- {child_class}\n")

        for related_class, classes in self.class_relationships.items():
            for instantiated_class in classes:
                if instantiated_class in self.classes and related_class != instantiated_class:
                    plantuml_file.write(f"{related_class} -- {instantiated_class}\n")
