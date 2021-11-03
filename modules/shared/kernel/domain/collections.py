from abc import ABC, abstractmethod
from typing import Generic, Iterable, Iterator, Tuple, Type, TypeVar

from pydantic.dataclasses import dataclass

__all__ = ('Collection', )

T = TypeVar('T')


@dataclass(init=False, repr=False, frozen=True)
class Collection(Generic[T], ABC):
    items: Tuple[T, ...]

    def __init__(self, items: Iterable[T] = ()):
        object.__setattr__(self, 'items', tuple(items))
        # TODO: check if to call `self.__post_init__()` is necessary

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}{self.items!r}'

    def __len__(self) -> int:
        return len(self.items)

    def __getitem__(self, key: int) -> T:
        return self.items[key]

    def __iter__(self) -> Iterator[T]:
        return iter(self.items)

    def __reversed__(self) -> Iterator[T]:
        return reversed(self.items)

    def __contains__(self, item: T) -> bool:
        return item in self.items

    @abstractmethod
    def type(self) -> Type[T]:
        ...
