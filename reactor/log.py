"""Logging functions"""

import logging

levels = {
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "none": logging.CRITICAL,
    "debug": logging.DEBUG
}
def setupLogger(level="error", filename=None, filemode="w"):
    """
    Sets up the basic logger and if `:param:filename` is set, then it will log
    to that file instead of stdout.

    :param level: str, the level to log
    :param filename: str, the file to log to
    """

    if not level or level not in levels:
        level = "error"

    logging.basicConfig(
        level=levels[level],
        format="[%(levelname)-8s] %(asctime)s %(module)s:%(lineno)d %(message)s",
        datefmt="%H:%M:%S",
        filename=filename,
        filemode=filemode
    )

def setLoggerLevel(level):
    """
    Sets the logger level.

    :param level: str, a string representing the desired level

    """
    if level not in levels:
        return

    global logger
    logger.setLevel(levels[level])

# Get the logger
logger = logging.getLogger("reactor")

# export logging functions
debug = logger.debug
error = logger.error
warning = logger.warning
info = logger.info