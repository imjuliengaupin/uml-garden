"""uml-garden module for plantuml class diagram generation"""

import sys

from constants import MIN_ARGS_REQUIRED
from uml_generator import UmlGenerator


class UmlGarden():
    """uml-garden container for plantuml class diagram generation"""

    def __init__(self, argvs: list[str]) -> None:
        self.run_uml_garden(argvs)

    def run_uml_garden(self, argvs: list[str]) -> None:
        """execute core uml-garden logic"""

        # if the minimum # of .py file argvs are provided, remove the default script path argument
        # NOTE this is so the program is only considering the .py files in the argvs list passed by the user
        if len(argvs) >= MIN_ARGS_REQUIRED:
            argvs.pop(0)
        else:
            sys.exit("insufficient number of argvs provided")

        gardener: UmlGenerator = UmlGenerator(argvs)

        # generate a plantuml class inheritance figure (.puml) from all .py files passed to the argvs list
        gardener.generate_plantuml_class_figure()

        # generate a plantuml class inheritance diagram (.png) using the .puml file
        gardener.generate_plantuml_class_diagram()
