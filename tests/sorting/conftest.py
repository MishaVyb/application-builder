import pytest

from app.core import settings
from app.schemas.builds import BuildsSchema
from app.schemas.tasks import TasksSchema


@pytest.fixture
def build(build_name: str):
    """Requested build from yaml file."""
    builds_schema = BuildsSchema.parse_yaml(settings.BUILDS_FILE_PATH)
    builds_store = builds_schema.as_store()
    return builds_store[build_name]


@pytest.fixture
def store():
    """Tasks store from yaml file."""
    tasks_schema = TasksSchema.parse_yaml(settings.TASKS_FILE_PATH)
    return tasks_schema.as_store()
