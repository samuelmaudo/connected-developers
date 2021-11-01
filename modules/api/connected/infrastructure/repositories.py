from modules.api.connected.domain.entities import ConnectionCheck, ConnectionChecks
from modules.api.connected.domain.repositories import ConnectionCheckRepository
from modules.api.connected.domain.values import CheckUser

__all__ = ('MySqlConnectionCheckRepository',)


class MySqlConnectionCheckRepository(ConnectionCheckRepository):

    async def save(self, check: ConnectionCheck) -> None:
        return None

    async def search_by_users(self, user_1: CheckUser, user_2: CheckUser) -> ConnectionChecks:
        return ConnectionChecks()
