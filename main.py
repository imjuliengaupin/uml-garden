#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""uml-garden module for program entry point"""

import sys

from uml_garden import UmlGarden


def main(argvs: list[str]) -> None:
    """uml-garden program entry point"""
    UmlGarden(argvs)


if __name__ == "__main__":
    # NOTE brew install java graphviz
    # NOTE pip3 install pylint autopep8
    main(sys.argv)
