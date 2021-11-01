from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import Field, validator
from pydantic.dataclasses import dataclass

__all__ = ('Value', 'Bool', 'DateTime', 'Int', 'Str', 'Uuid')


@dataclass(repr=False, frozen=True)
class Value:
    value: Any

    def __repr__(self):
        return f'{self.__class__.__name__}({self.value!r})'


@dataclass(repr=False, frozen=True)
class Bool(Value):
    value: bool

    def __str__(self) -> str:
        return str(getattr(self, 'value')).lower()


@dataclass(repr=False, frozen=True)
class DateTime(Value):
    value: datetime

    def __str__(self) -> str:
        return getattr(self, 'value').isoformat()


@dataclass(repr=False, frozen=True)
class Int(Value):
    value: int

    def __str__(self) -> str:
        return str(getattr(self, 'value'))


@dataclass(repr=False, frozen=True)
class PositiveInt(Int):
    value: int = Field(ge=0)


@dataclass(repr=False, frozen=True)
class Str(Value):
    value: str

    def __str__(self) -> str:
        return getattr(self, 'value')


@dataclass(repr=False, frozen=True)
class Uuid(Value):
    value: UUID = Field(default_factory=uuid4)

    def __str__(self) -> str:
        return str(getattr(self, 'value'))


@dataclass(repr=False, frozen=True)
class Uuid(Str):

    @staticmethod
    def check_uuid(v: str) -> bool:
        try:
            UUID(v)
        except ValueError:
            return False
        else:
            return True

    @classmethod
    def random(cls) -> 'Uuid':
        return cls(str(uuid4()))

    @validator('value')
    def validate_uuid(cls, v: str) -> str:
        assert cls.check_uuid(v), f'{v} is not a UUID'
        return v
