from datetime import datetime
from typing import Any, Dict, Iterable, Type

from pydantic import Field

from modules.api.connected.domain.values import *
from modules.shared.kernel.domain.collections import Collection
from modules.shared.kernel.domain.entities import Entity

__all__ = ('ConnectionCheck', 'ConnectionChecks')


class ConnectionCheck(Entity):
    id: CheckId = Field(..., allow_mutation=False)
    registered_at: CheckRegistrationDateTime
    users: CheckUsers
    connected: CheckConnected
    organisations: CheckOrganisations

    def identity(self) -> CheckId:
        return self.id

    @classmethod
    def store(
        cls,
        id: CheckId,
        registered_at: CheckRegistrationDateTime,
        user_1: CheckUser,
        user_2: CheckUser,
        organisations: CheckOrganisations
    ) -> 'ConnectionCheck':
        return cls(
            id=id,
            registered_at=registered_at,
            users=CheckUsers([user_1, user_2]),
            connected=CheckConnected(bool(organisations)),
            organisations=organisations)

    @classmethod
    def from_primitives(
        cls,
        id: str,
        registered_at: datetime,
        user_1: str,
        user_2: str,
        organisations: Iterable[str]
    ) -> 'ConnectionCheck':
        return cls(
            id=CheckId(id),
            registered_at=CheckRegistrationDateTime(registered_at),
            users=CheckUsers([CheckUser(user_1), CheckUser(user_2)]),
            connected=CheckConnected(bool(organisations)),
            organisations=CheckOrganisations([
                CheckOrganisation(organisation)
                for organisation
                in organisations
            ]))

    def to_primitives(self) -> Dict[str, Any]:
        return {
            'id': self.id.value,
            'registered_at': self.registered_at.value,
            'user_1': self.users[0].value,
            'user_2': self.users[1].value,
            'organisations': [
                organisation.value
                for organisation
                in self.organisations
            ]
        }


class ConnectionChecks(Collection[ConnectionCheck]):

    def type(self) -> Type[ConnectionCheck]:
        return ConnectionCheck
