from abc import ABC, abstractmethod
from typing import Generic, Iterable, Tuple, TypeVar

__all__ = ('DomainError', 'NotFoundError', 'AggregatedError')

T = TypeVar('T')


class DomainError(Exception, ABC):

    def __init__(self):
        super().__init__(self.error_message())

    @abstractmethod
    def error_code(self) -> str:
        ...

    @abstractmethod
    def error_message(self) -> str:
        ...


class NotFoundError(Generic[T], DomainError, ABC):

    def __init__(self, key: T):
        self._key = key
        super().__init__()

    @property
    def key(self) -> T:
        return self._key


class AggregatedError(Generic[T], DomainError, ABC):

    def __init__(self, errors: Iterable[T]):
        self._errors = tuple(errors)
        super().__init__()

    @property
    def errors(self) -> Tuple[T]:
        return self._errors
