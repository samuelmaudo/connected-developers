from typing import Dict, List, Tuple

from tortoise import fields
from tortoise.models import Model as Table

from modules.api.connected.domain.entities import ConnectionCheck, ConnectionChecks
from modules.api.connected.domain.repositories import ConnectionCheckRepository
from modules.api.connected.domain.values import CheckUser

__all__ = ('TortoiseConnectionCheckRepository', 'DummyConnectionCheckRepository')


class TortoiseConnectionCheckRepository(ConnectionCheckRepository):

    async def save(self, check: ConnectionCheck) -> None:
        data = check.to_primitives()
        users = sorted([data['user_1'], data['user_2']])
        data['user_1'] = users[0]
        data['user_2'] = users[1]
        row = TortoiseConnectionCheckTable(**data)
        await row.save()

    async def search_by_users(self, user_1: CheckUser, user_2: CheckUser) -> ConnectionChecks:
        users = sorted([user_1.value, user_2.value])
        rows = await TortoiseConnectionCheckTable.filter(
            user_1=users[0],
            user_2=users[1],
        )
        checks = (
            ConnectionCheck.from_primitives(
                str(row.id),
                row.registered_at,
                row.user_1,
                row.user_2,
                row.organisations
            )
            for row
            in rows
        )
        return ConnectionChecks(checks)


class TortoiseConnectionCheckTable(Table):

    id = fields.UUIDField(pk=True)
    registered_at = fields.DatetimeField()
    user_1 = fields.CharField(max_length=255)
    user_2 = fields.CharField(max_length=255)
    organisations = fields.JSONField()

    class Meta:
        table = 'api_connection_check'
        indexes = (('user_1', 'user_2'),)


class DummyConnectionCheckRepository(ConnectionCheckRepository):

    _connection_checks: Dict[Tuple[str, ...], List[ConnectionCheck]] = {}

    async def save(self, check: ConnectionCheck) -> None:
        users = tuple(sorted(user.value for user in check.users))
        if users not in self._connection_checks:
            self._connection_checks[users] = []

        self._connection_checks[users].append(check)

    async def search_by_users(self, user_1: CheckUser, user_2: CheckUser) -> ConnectionChecks:
        users = tuple(sorted([user_1.value, user_2.value]))
        if users not in self._connection_checks:
            return ConnectionChecks()

        return ConnectionChecks(self._connection_checks[users])
