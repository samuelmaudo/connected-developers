from typing import Type

from modules.shared.kernel.domain.collections import Collection
from modules.shared.kernel.domain.values import Bool, DateTime, Str, Uuid

__all__ = (
    'CheckId',
    'CheckRegistrationDateTime',
    'CheckUser', 'CheckUsers',
    'CheckConnected',
    'CheckOrganisation', 'CheckOrganisations'
)


class CheckId(Uuid):
    ...


class CheckRegistrationDateTime(DateTime):
    ...


class CheckUser(Str):
    ...


class CheckUsers(Collection[CheckUser]):

    def type(self) -> Type[CheckUser]:
        return CheckUser


class CheckConnected(Bool):
    ...


class CheckOrganisation(Str):
    ...


class CheckOrganisations(Collection[CheckOrganisation]):

    def type(self) -> Type[CheckOrganisation]:
        return CheckOrganisation
