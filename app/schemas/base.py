from __future__ import annotations


import yaml
from pydantic import BaseModel, Field, FilePath, PydanticValueError
from pydantic.validators import dict_validator

from app.core import settings


class BaseSchema(BaseModel):
    @classmethod
    def parse_yaml(cls, path: FilePath | str, *, key: str | None = None):
        with open(path, 'r') as file:
            content = yaml.safe_load(file)
        return cls.parse_obj(content)

        # if not key:
        #     return cls.parse_obj(content)

        # content = dict_validator(content)
        # if key not in content:
        #     # FIXME
        #     raise PydanticValueError(
        #         f'Target field "{key}" not present in yaml file: {path}. '
        #     )

        # return cls.parse_obj(content[key])
