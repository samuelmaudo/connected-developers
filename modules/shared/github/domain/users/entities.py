from typing import Any, Dict, Type

from pydantic import Field

from modules.shared.github.domain.users.values import *
from modules.shared.kernel.domain.collections import Collection
from modules.shared.kernel.domain.entities import Entity

__all__ = ('User', 'Organization', 'Organizations')


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


class Organization(Entity):
    id: OrganizationId = Field(..., allow_mutation=False)
    login: OrganizationLogin

    def identity(self) -> OrganizationId:
        return self.id

    @classmethod
    def from_primitives(cls, id: int, login: str) -> 'Organization':
        return cls(id=OrganizationId(id), login=OrganizationLogin(login))

    def to_primitives(self) -> Dict[str, Any]:
        return {'id': self.id.value, 'login': self.login.value}


class Organizations(Collection[Organization]):

    def type(self) -> Type[Organization]:
        return Organization
