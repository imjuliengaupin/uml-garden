
import logging

# debugging
DEBUG_MODE: bool = True
LOGGER: logging.Logger = logging.getLogger(__name__)

# paths
LOGS_PATH: str = "./logs"
PLANTUMLS: str = "./plantuml"

# uml_garden.py
MIN_ARGS_REQUIRED: int = 2

# uml_generator.py
UML_OPEN: str = "@startuml"
UML_CLOSE: str = "@enduml"
