from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel

__all__ = ('Entity',)


class Entity(BaseModel, ABC):

    class Config:
        validate_assignment = True

    def __eq__(self, other: Any) -> bool:
        if other.__class__ != self.__class__:
            raise NotImplementedError

        return other.identity() == self.identity()

    def __hash__(self) -> int:
        return hash((self.__class__, self.identity()))

    @abstractmethod
    def identity(self) -> Any:
        ...
