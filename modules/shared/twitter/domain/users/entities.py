from typing import Any, Dict, Type

from pydantic import Field

from modules.shared.kernel.domain.collections import Collection
from modules.shared.kernel.domain.entities import Entity
from modules.shared.twitter.domain.users.values import *

__all__ = ('User', 'Users')


class User(Entity):
    id: UserId = Field(..., allow_mutation=False)
    login: UserLogin

    def identity(self) -> UserId:
        return self.id

    @classmethod
    def from_primitives(cls, id: int, login: str) -> 'User':
        return cls(id=UserId(id), login=UserLogin(login))

    def to_primitives(self) -> Dict[str, Any]:
        return {'id': self.id.value, 'login': self.login.value}


class Users(Collection[User]):

    def type(self) -> Type[User]:
        return User
