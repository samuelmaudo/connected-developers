from abc import ABC, abstractmethod
from typing import Generic, Iterable, Iterator, Tuple, Type, TypeVar

from pydantic.dataclasses import dataclass

__all__ = ('Collection', )

T = TypeVar('T')


@dataclass(init=False, repr=False, frozen=True)
class Collection(Generic[T], ABC):

    items: Tuple[T, ...]

    def __init__(self, items: Iterable[T] = ()):
        items = tuple(items)
        type_ = self.type()
        for item in items:
            if not isinstance(item, type_):
                raise TypeError(f'{self.__class__.__name__} can only content instances of {type_.__name__}')

        object.__setattr__(self, 'items', items)

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
