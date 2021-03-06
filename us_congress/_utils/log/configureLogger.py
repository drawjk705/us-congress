import logging
import sys

from us_congress._utils.log.filters import ModuleFilter

DEFAULT_LOGFILE = "congress.log"


def configureLogger(logFile: str) -> None:
    """
    sets up logger for the project

    Args:
        logFile (str): the name of the file that log output will be sent to
    """

    logFormat = (
        "[%(levelname)s] %(asctime)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s"
    )
    dateFormat = "%Y-%m-%d %H:%M:%S%z"

    logger = logging.getLogger("census")
    logger.setLevel(logging.NOTSET)

    streamHandler = logging.StreamHandler(sys.stdout)
    streamHandler.setLevel(logging.INFO)
    formatter = logging.Formatter(logFormat, datefmt=dateFormat)
    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)

    rootHandler = logging.FileHandler(logFile)
    rootHandler.setLevel(logging.NOTSET)
    rootHandler.addFilter(ModuleFilter())
    rootHandler.setFormatter(formatter)

    logging.basicConfig(level=logging.DEBUG, format=logFormat, handlers=[rootHandler])
