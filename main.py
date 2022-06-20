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
    main(sys.argv)
