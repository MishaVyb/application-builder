import time
from contextlib import contextmanager
from typing import Callable

from app.core import logger


@contextmanager
def timer(name: str = '', log: Callable = logger.debug):
    name = name or 'timer'
    start_time = time.time()
    try:
        log(f'Start [{name}]. ')
        yield
    finally:
        stop_time = time.time()
        log(f'Stop [{name}]. It takes: {stop_time - start_time}.')
