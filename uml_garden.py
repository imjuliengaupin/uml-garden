
import sys

from constants import MIN_ARGS_REQUIRED


class UmlGarden(object):

    def __init__(self, argvs: list[str]) -> None:
        self.run_uml_garden(argvs)

    def run_uml_garden(self, argvs: list[str]) -> None:
        argvs.pop(0) if len(argvs) >= MIN_ARGS_REQUIRED else sys.exit(f"insufficient number of argvs provided")
