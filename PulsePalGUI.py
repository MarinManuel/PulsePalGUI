import argparse
import logging

from PyQt5.QtWidgets import QApplication

from src.PulsePal import PulsePalObject, PulsePalError
from src.PulsePalGUI import (
    MainWindow,
    discover_ports,
    DummyPulsePalObject,
    choose_port_dialog,
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
        help="the serial port used to communicate with the Pulse Pal. If not provided, "
        "then the software will try to find the port automatically, and/or offer "
        "a choice of possible ports",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="increase verbosity of output (can be "
        "repeated to increase verbosity further)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        dest="debug_mode",
        help="use a dummy pulsepal simulator instead of the real hardware",
    )
    args = parser.parse_args()

    level = LOGGING_LEVELS[
        min(args.verbose, len(LOGGING_LEVELS) - 1)
    ]  # cap to last level index
    logger.setLevel(level=level)

    if args.port is None:
        logger.info("Starting serial port auto-discovery...")
        possible_ports = discover_ports()
        if len(possible_ports) > 1:
            # there are more than 1 valid port.
            logger.info(
                f"Found serial ports {','.join([p.device for p in possible_ports])}. Asking user to choose one"
            )
            args.port = choose_port_dialog(possible_ports)
        elif len(possible_ports) == 1:
            args.port = possible_ports[0].device
            logger.info(f"Found serial port [{args.port}]")
        else:
            args.port = None

    if args.port is None and not args.debug_mode:
        raise PulsePalError(
            "Could not find a suitable serial port. Please provide the serial port using the "
            "--port argument"
        )

    if args.debug_mode:
        pulsepal = DummyPulsePalObject(None)
        logger.info(f"Running in debug mode with Dummy Pulse Pal device: {pulsepal}")
    else:
        pulsepal = PulsePalObject(args.port)
        logger.debug(f"Connecting to serial port [{args.port}]: {pulsepal}")

    app = QApplication([])
    mw = MainWindow(pulsepal)
    mw.show()
    # Start the event loop.
    app.exec()
