from pydantic import BaseModel


class GetTasksSchemaIn(BaseModel):
    build: str
    """Build name. """
