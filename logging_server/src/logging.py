import sys
import logging


def setup_basic_logging():
    level = logging.INFO
    formatter = logging.Formatter("%(asctime)s %(levelname)-8s %(name)s: %(message)s")

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    handler.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(level)
    root.addHandler(handler)
