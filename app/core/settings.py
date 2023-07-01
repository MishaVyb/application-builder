import logging
from pathlib import Path

from pydantic import BaseSettings, DirectoryPath, FilePath


class Settings(BaseSettings):
    DEBUG: bool = False
    BASEDIR: DirectoryPath = Path(__file__).resolve().parent.parent.parent
    BUILDS_FILE_PATH: FilePath = BASEDIR / 'builds' / 'builds.yaml'
    TASKS_FILE_PATH: FilePath = BASEDIR / 'builds' / 'tasks.yaml'
    LOG_LEVEL: int | str = logging.INFO

    class Config:
        allow_mutations = False


# App settings:
settings = Settings()

# Log settings:
logger = logging.getLogger(__name__)
logger.setLevel(settings.LOG_LEVEL)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
logger.addHandler(handler)
