from typing import TypeAlias

import yaml
from pydantic import BaseModel, FilePath


class BaseSchema(BaseModel):
    @classmethod
    def parse_yaml(cls, path: FilePath | str):
        with open(path, 'r') as file:
            content = yaml.safe_load(file)
        return cls.parse_obj(content)


TaskName: TypeAlias = str
