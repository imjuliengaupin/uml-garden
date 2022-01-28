#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from uml_garden import UmlGarden


def main(argvs: list[str]) -> None:
    UmlGarden(argvs)


if __name__ == "__main__":
    main(sys.argv)
