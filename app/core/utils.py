import time
from contextlib import contextmanager

from app.core import logger


@contextmanager
def timer(name: str = ''):
    name = name or 'timer'
    start_time = time.time()
    try:
        logger.info(f'Start [{name}]. ')
        yield
    finally:
        stop_time = time.time()
        logger.info(f'Stop [{name}]. It takes: {stop_time - start_time}.')
