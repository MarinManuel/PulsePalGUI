import argparse
import logging

from PyQt5.QtWidgets import QApplication

from src.PulsePal import PulsePalObject, PulsePalError
from src.PulsePalGUI import (
    MainWindow,
    DummyPulsePalObject,
)

logger = logging.getLogger("PulsePalGUI")
handler = logging.StreamHandler()
# noinspection SpellCheckingInspection
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
LOGGING_LEVELS = [logging.NOTSET, logging.WARNING, logging.INFO, logging.DEBUG]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="PulsePalGUI",
        description="This software provides a graphical user interface for controlling a Pulse Pal, an open source "
        "pulse train generator for physiology and behavior",
    )
    parser.add_argument(
        "-p",
        "--port",
        help="the serial port used to communicate with the Pulse Pal",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="increase verbosity of output (can be "
        "repeated to increase verbosity further)",
    )
    args = parser.parse_args()

    level = LOGGING_LEVELS[
        min(args.verbose, len(LOGGING_LEVELS) - 1)
    ]  # cap to last level index
    logger.setLevel(level=level)

    if args.port is None:
        logger.info("Starting PulsePalGUI with no serial port.")
        pulsepal = DummyPulsePalObject(None)
    else:
        logger.info("Starting PulsePalGUI with serial port '{}'".format(args.port))
        pulsepal = PulsePalObject(args.port)

    app = QApplication([])
    mw = MainWindow(pulsepal)
    mw.show()
    # Start the event loop.
    app.exec()
