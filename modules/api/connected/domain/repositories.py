from modules.api.connected.domain.entities import ConnectionCheck, ConnectionChecks
from modules.api.connected.domain.values import CheckUser

__all__ = ('ConnectionCheckRepository',)


class ConnectionCheckRepository:

    async def save(self, check: ConnectionCheck) -> None:
        raise NotImplementedError

    async def search_by_users(self, user_1: CheckUser, user_2: CheckUser) -> ConnectionChecks:
        raise NotImplementedError
