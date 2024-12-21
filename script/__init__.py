import logging
import os

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def setup_logging(level=logging.INFO):
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


setup_logging()
