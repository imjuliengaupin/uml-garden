"""uml-garden module for .py code scan logic and plantuml class figure generation"""

import io
import os
import re as regex
import subprocess
import sys

from constants import PLANTUMLS, UML_OPEN, UML_CLOSE


class UmlGenerator():
    """uml-garden container for .py code scan logic and plantuml class figure generation"""

    def __init__(self, py_files: list[str]) -> None:
        self.py_files: list[str] = py_files
        self.class_name: str = ""
        self.classes: list = []
        self.class_variables: dict = {}
        self.class_relationships: dict = {}
        self.parents: dict = {}

        self.compile_regex_patterns()

    def compile_regex_patterns(self) -> None:
        """compile regular expression patterns for python code scan logic"""

        self.is_newline_found: regex.Pattern = regex.compile(r"^\s*(:?$|#|raise|print)")
        self.is_base_class_found: regex.Pattern = regex.compile(r"^class\s+([\w\d]+)\(\)\s*:")
        self.is_child_class_found: regex.Pattern = regex.compile(r"^class\s+([\w\d]+)\(\s*([\w\d\._]+)\s*\):")
        self.is_class_variable_found: regex.Pattern = regex.compile(r"^\s+self.([_\w]+)\s*=")
        self.is_private_class_variable_found: regex.Pattern = regex.compile(r"^__[\w\d_]+")
        self.is_protected_class_variable_found: regex.Pattern = regex.compile(r"^_[\w\d_]+")
        self.is_builtin_class_method_found: regex.Pattern = regex.compile(r"^__[\w_]+__")
        self.is_class_method_found: regex.Pattern = regex.compile(r"^\s+def (\w+)\(.*\):")
        self.is_private_class_method_found: regex.Pattern = regex.compile(r"^__[\w_]+")
        self.is_protected_class_method_found: regex.Pattern = regex.compile(r"^_[\w_]+")
        self.is_instantiated_class_found: regex.Pattern = regex.compile(r"((:?[A-Z]+[a-z0-9]+)+)\(.*\)")

    def get_package_name(self, index: int) -> str:
        """extract the name of the .py file passed as an argv to the argvs list to be used as the package name"""
        return os.path.basename(self.py_files[index].split('.')[0])

    def get_class_variable_access_modifier_uml_notation(self, class_variable_name: str) -> str:
        """define the uml representation for class variables with access modifiers"""

        # for private class variables, e.g. self.__var
        if self.is_private_class_variable_found.match(class_variable_name):
            return '-' + class_variable_name

        # for protected class variables, e.g. self._var
        if self.is_protected_class_variable_found.match(class_variable_name):
            return '#' + class_variable_name

        # for public class variables, e.g. self.var
        return '+' + class_variable_name

    def get_class_method_access_modifier_uml_notation(self, class_method_name: str) -> str:
        """define the uml representation for class methods (including built-in methods) with access modifiers"""

        # for built-in class methods, e.g. __init__(), __str__(), etc.
        if self.is_builtin_class_method_found.match(class_method_name):
            return '+' + class_method_name

        # for private class methods, e.g. __method()
        if self.is_private_class_method_found.match(class_method_name):
            return '-' + class_method_name

        # for protected class methods, e.g. _method()
        if self.is_protected_class_method_found.match(class_method_name):
            return '#' + class_method_name

        # for public class methods, e.g. method()
        return '+' + class_method_name

    def set_class_variables(self, class_variable_name: str) -> None:
        """append all instances of a class variable with access modifier details to a dictionary"""

        # extract the access modifier for the class variable
        class_variable = self.get_class_variable_access_modifier_uml_notation(class_variable_name)

        # if the class variable identified is not already apart of the class variables dictionary ...
        if class_variable not in self.class_variables[self.class_name]:
            # ... append the class variable and access modifier
            self.class_variables[self.class_name].append(class_variable)

    def set_class_instantiation_relationships(self, instantiated_class_name: str) -> None:
        """append all instances of a class being instantiated in an external class file to a dictionary"""

        # if the instantiated class name identified is not already apart of the class relationships dictionary ...
        if instantiated_class_name not in self.class_relationships[self.class_name]:
            # ... append the instantiated class name and it's relationship
            self.class_relationships[self.class_name].append(instantiated_class_name)

    def generate_plantuml_class_figure(self) -> None:
        """execute .py code scan logic to extract and write out uml syntax to a .puml file in the local project directory"""

        # create a folder in the local project directory to store the output .puml file ...
        if not os.path.exists(PLANTUMLS):
            os.makedirs(PLANTUMLS)

        # create a new .puml file in the local project directory to write to ...
        with open(f"{PLANTUMLS}/uml-garden.puml", 'w', encoding="utf8") as plantuml_file:
            # ... write out the conventional uml file header to the new .puml file created
            plantuml_file.write(f"{UML_OPEN}\n")

            # for each .py file passed to the program argvs list ...
            for py_file in self.py_files:
                # ... validate whether or not the argv passed is a file
                if '.' not in py_file:
                    sys.exit("folder argvs are unsupported")

                # ... capture the argv index position in the argvs list
                index: int = self.py_files.index(py_file)

                # ... write out the .py package name to the new .puml file created
                self.write_package_name_uml_notation(plantuml_file, index)

                # ... run .py code scan logic and write out the .py class methods to the new .puml file created
                self.python_code_scan(plantuml_file, py_file)

                # ... write out the .py class variables to the new .puml file created
                self.write_class_variables_uml_notation(plantuml_file)

            # ... write out the .py class relationships to the new .puml file created
            self.write_class_relationships_uml_notation(plantuml_file)

            # ... write out the conventional uml file footer to the new .puml file created
            plantuml_file.write(f"{UML_CLOSE}\n")

    def generate_plantuml_class_diagram(self) -> None:
        """execute a java plantuml.jar subprocess to generate a plantuml diagram .png in the local project directory"""
        plantuml_file_path: str = f"{PLANTUMLS}/uml-garden.puml"
        subprocess.call(["java", "-jar", "plantuml.jar", plantuml_file_path])

    def python_code_scan(self, plantuml_file: io.TextIOWrapper, py_file: str) -> None:
        """scan python code files to extract uml class figure details"""

        for line_of_code in open(py_file, 'r', encoding="utf8"):
            # #######################################################################
            # if a newline "\n" is found in the code file being read, ignore it

            if self.is_newline_found.match(line_of_code):
                continue

            # #######################################################################
            # if any code for a class that does not have a parent is found

            # match the regex string result to a pattern matching a defined base class, e.g. class Parent():
            base_class_found = self.is_base_class_found.match(line_of_code)

            # if a pattern is found that matches a defined base class ...
            if base_class_found:
                # ... save the base class name
                base_class_name = base_class_found.group(1)

                # ... write out the base (parent) or child class name to the new .puml file created
                self.write_class_name_uml_notation(plantuml_file, base_class_name, "")

                continue

            # #######################################################################
            # if any code for a class that has a parent is found

            # match the regex string result to a pattern matching a defined parent-child class relationship, e.g. class Parent(Child):
            child_class_found = self.is_child_class_found.match(line_of_code)

            # if a pattern is found that matches a defined parent-child class relationship ...
            if child_class_found:
                # ... save the parent and child class names
                # NOTE https://docs.python.org/3/library/re.html#re.Match.group
                child_class_name = child_class_found.group(1)
                parent_class_name = child_class_found.group(2)

                # ... write out the base (parent) or child class name to the new .puml file created
                self.write_class_name_uml_notation(plantuml_file, child_class_name, parent_class_name)

                continue

            # #######################################################################
            # if any class variable definition or initialization code is found

            # match the regex string result to a pattern matching the definition or initialization of a class variable
            class_variable_found = self.is_class_variable_found.match(line_of_code)

            # if a pattern is found that matches the definition or initialization of a class variable ...
            if class_variable_found and self.class_name:
                # ... save the class variable name
                class_variable_name = class_variable_found.group(1)

                # ... append the class variable name and access modifier to the list of class variables
                self.set_class_variables(class_variable_name)

                continue

            # #######################################################################
            # if any class method definition or instantiation code is found

            # match the regex string result to a pattern matching the definition or instantiation of a class method
            class_method_found = self.is_class_method_found.match(line_of_code)

            # if a pattern is found that matches defining or instantiating a class method ...
            if class_method_found and self.class_name:
                # ... save the class method name
                class_method_name = class_method_found.group(1)

                # ... write out the class method name and access modifier to the new .puml file created
                self.write_class_methods_uml_notation(plantuml_file, class_method_name)

                continue

            # #######################################################################
            # if any class object instantiation code is found

            # search the regex string result for a pattern matching class object instantiation
            # NOTE https://docs.python.org/3/library/re.html#search-vs-match
            # NOTE https://docs.python.org/3/library/re.html#re.search
            class_instantiation_found = self.is_instantiated_class_found.search(line_of_code)

            # if a pattern is found that matches class object instantiation ...
            if class_instantiation_found and self.class_name:
                # ... save the instantiated class name
                instantiated_class_name = class_instantiation_found.group(1)

                # ... append the instantiated class name to the list of class relationships
                self.set_class_instantiation_relationships(instantiated_class_name)

                continue

    def write_package_name_uml_notation(self, plantuml_file: io.TextIOWrapper, index: int) -> None:
        """write .py package name to the generated .puml file"""

        # extract the package name from the .py file passed as an argument to the argvs list
        package_name: str = self.get_package_name(index)

        self.class_name = None
        self.class_variables = {}

        # write out the .py package name uml to the new .puml file created
        plantuml_file.write(f"package {package_name} {{\n")

    def write_class_name_uml_notation(self, plantuml_file: io.TextIOWrapper, base_or_child_class_name: str, parent_class_name: str) -> None:
        """write .py class name to the generated .puml file"""

        # if the base (or child) class name is already present in the classes list ...
        if base_or_child_class_name in self.classes:
            # ... ignore it and continue to scan .py code until a class name is found that is not yet in the list
            return

        # save the base (or child) class name to the classes list
        self.classes.append(base_or_child_class_name)

        self.class_name = base_or_child_class_name

        # initialize class variable dictionary for the base (or child) class, e.g. { class : [variable, variable, ...] }
        self.class_variables[base_or_child_class_name] = []

        # initialize parent-child class relationship dictionary for the base (or child) class, e.g. { parent : child }
        self.parents[base_or_child_class_name] = parent_class_name

        # initialize class relationship dictionary for the base (or child) class, e.g. { class : [relationship, relationship, ...] }
        self.class_relationships[base_or_child_class_name] = []

        # write out the class name uml to the new .puml file created
        plantuml_file.write(f"class {base_or_child_class_name}\n")

    def write_class_variables_uml_notation(self, plantuml_file: io.TextIOWrapper) -> None:
        """write .py class variables with access modifier details in uml format to the generated .puml file"""

        # for each of the classes and class members (variables) ...
        for class_name, class_members in self.class_variables.items():
            # for each class variable in the list of class members ...
            for class_variable in class_members:
                # ... write out the class variable and access modifier uml to the new .puml file created
                plantuml_file.write(f"{class_name} : {class_variable}\n")

        plantuml_file.write("}\n\n")

    def write_class_methods_uml_notation(self, plantuml_file: io.TextIOWrapper, class_method_name: str) -> None:
        """write .py class methods (including built-in methods) with access modifier details in uml format to the generated .puml file"""

        # extract the access modifier for the class method
        class_method_name = self.get_class_method_access_modifier_uml_notation(class_method_name)

        # write out the class method uml to the new .puml file created
        plantuml_file.write(f"{self.class_name} : {class_method_name}()\n")

    def write_class_relationships_uml_notation(self, plantuml_file: io.TextIOWrapper) -> None:
        """write .py class relationships in uml format to the generated .puml file"""

        # for each of the parent and child classes ...
        for child_class, parent_class in self.parents.items():
            # if a child class does not have a parent class, or if a parent class inherits from object ...
            if not parent_class or parent_class == "object":
                # ... ignore it and continue to the next class in the list
                continue

            # write out the parent-child class relationship uml to the new .puml file created
            plantuml_file.write(f"{parent_class} <|-- {child_class}\n")

        # for each class that contains a defined instantiated class object ...
        for related_class, classes in self.class_relationships.items():
            # for each of the instantiated class objects identified ...
            for instantiated_class in classes:
                if instantiated_class in self.classes and related_class != instantiated_class:
                    # ... write out the instantiated class objects relationship uml to the new .puml file created
                    plantuml_file.write(f"{related_class} -- {instantiated_class}\n")
