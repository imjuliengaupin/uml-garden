
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
        self.is_child_class_found: regex.Pattern = regex.compile(r"^class\s+([\w\d]+)\(\s*([\w\d\._]+)\s*\):")
        self.is_class_variable_found: regex.Pattern = regex.compile(r"^\s+self.([_\w]+)\s*=")
        self.is_private_class_variable_found: regex.Pattern = regex.compile(r"^__[\w\d_]+")
        self.is_protected_class_variable_found: regex.Pattern = regex.compile(r"^_[\w\d_]+")
        self.is_class_method_found: regex.Pattern = regex.compile(r"^\s+def (\w+)\(.*\):")

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

                self.write_core_uml_content(plantuml_file, py_file)

                self.write_post_uml_content(plantuml_file)

            self.write_post_uml_relationship_content(plantuml_file)

            # write out the conventional uml file footer to the new .puml file created
            plantuml_file.write(f"{UML_CLOSE}\n")

    def get_class_variable_uml_notation(self, class_variable_name: str) -> str:

        # for private class variables, e.g. self.__var
        if self.is_private_class_variable_found.match(class_variable_name):
            return '-' + class_variable_name
        # for protected class variables, e.g. self._var
        elif self.is_protected_class_variable_found.match(class_variable_name):
            return '#' + class_variable_name
        # for public class variables, e.g. self.var
        else:
            return '+' + class_variable_name

    def get_class_method_uml_notation(self, class_method_name: str) -> str:
        ...

    def set_class_name_uml_notation(self, plantuml_file: io.TextIOWrapper, base_or_child_class_name: str, parent_class_name: str) -> None:

        if base_or_child_class_name in self.classes:
            return

        self.classes.append(base_or_child_class_name)

        self.class_relationships[base_or_child_class_name] = []
        self.parents[base_or_child_class_name] = parent_class_name
        self.class_name = base_or_child_class_name  # no type hinting recommended
        self.class_variables[base_or_child_class_name] = []

        plantuml_file.write(f"class {base_or_child_class_name}\n")

    def set_class_variable_uml_notation(self, class_variable_name: str) -> None:

        class_variable = self.get_class_variable_uml_notation(class_variable_name)

        if class_variable not in self.class_variables[self.class_name]:
            self.class_variables[self.class_name].append(class_variable)

    def set_class_method_uml_notation(self, plantuml_file: io.TextIOWrapper, class_method_name: str) -> None:

        class_method_name = self.get_class_method_uml_notation(class_method_name)

        plantuml_file.write(f"{self.class_name} : {class_method_name}()\n")

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

            # if a class that has a parent is found
            child_class_found = self.is_child_class_found.match(line_of_code)

            if child_class_found:
                # NOTE https://docs.python.org/3/library/re.html#re.Match.group
                child_class_name = child_class_found.group(1)
                parent_class_name = child_class_found.group(2)

                self.set_class_name_uml_notation(plantuml_file, child_class_name, parent_class_name)

                continue

            # if a class variable is found
            class_variable_found = self.is_class_variable_found.match(line_of_code)

            if class_variable_found and self.class_name:
                class_variable_name = class_variable_found.group(1)
            
                self.set_class_variable_uml_notation(class_variable_name)

                # TEST add a continue statement here ?

            # if a class method is found
            class_method_found = self.is_class_method_found.match(line_of_code)

            if class_method_found and self.class_name:
                class_method_name = class_method_found.group(1)

                self.set_class_method_uml_notation(plantuml_file, class_method_name)

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
