#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

from constants import logging, DEBUG_MODE, LOGGER, LOGS_PATH
from uml_garden import UmlGarden


def main(argvs: list[str]) -> None:
    "main()"
    UmlGarden(argvs)


if __name__ == "__main__":
    if DEBUG_MODE:
        if not os.path.exists(LOGS_PATH):
            os.makedirs(LOGS_PATH)

        # NOTE https://docs.python.org/3/library/logging.html#logrecord-attributes
        formatter: logging.Formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")
        handler: logging.FileHandler = logging.FileHandler(f"{LOGS_PATH}/uml-garden-argvs.log")

        handler.setFormatter(formatter)

        LOGGER.addHandler(handler)
        LOGGER.setLevel(logging.DEBUG)
        LOGGER.debug(f"{main.__doc__}".replace("()", f"(argvs={sys.argv})"))

    main(sys.argv)