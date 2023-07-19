from abc import ABC

from pydantic import BaseModel


class AbstractModel(ABC, BaseModel):
    pass
