from typing import Optional

from modules.shared.github.domain.users.entities import *
from modules.shared.github.domain.users.values import *

__all__ = ('UserRepository',)


class UserRepository:

    async def find_by_login(self, login: UserLogin) -> Optional[User]:
        raise NotImplementedError

    async def search_organizations(self, user: User) -> Organizations:
        return await self.search_organizations_by_login(user.login)

    async def search_organizations_by_login(self, login: UserLogin) -> Organizations:
        raise NotImplementedError
