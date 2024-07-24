import argparse
import logging
import sys

from PyQt5.QtWidgets import QApplication, QMessageBox

from src.ArCOM import ArCOMError
from src.PulsePal import PulsePalObject
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

    app = QApplication([])

    if args.port is None:
        logger.info("Starting PulsePalGUI with no serial port.")
        pulsepal = DummyPulsePalObject(None)
    else:
        logger.info("Starting PulsePalGUI with serial port '{}'".format(args.port))
        try:
            pulsepal = PulsePalObject(args.port)
        except ArCOMError as e:
            # noinspection PyTypeChecker
            QMessageBox.critical(None, "Critical error",
                                 f"Could not communicate with Pulse Pal on {args.port}:\n{e}")
            sys.exit(1)

    mw = MainWindow(pulsepal)
    mw.show()
    # Start the event loop.
    app.exec()
