
import sys

from constants import DEBUG_MODE, LOGGER, MIN_ARGS_REQUIRED
from uml_generator import UmlGenerator


class UmlGarden(object):

    def __init__(self, argvs: list[str]) -> None:
        self.run_uml_garden(argvs)

    def run_uml_garden(self, argvs: list[str]) -> None:
        # if the minimum # of .py file argvs are provided, remove the default script path argument
        # so the program is only considering the .py files in the argvs list passed by the user
        argvs.pop(0) if len(argvs) >= MIN_ARGS_REQUIRED else sys.exit(f"insufficient number of argvs provided")

        gardener: UmlGenerator = UmlGenerator(argvs)

        if DEBUG_MODE:
            LOGGER.debug(gardener.generate_plantuml_class_figure.__doc__)

        # generate a .puml class inheritance diagram for the .py files passed to the argvs list
        gardener.generate_plantuml_class_figure()

        gardener.generate_plantuml_diagram()
