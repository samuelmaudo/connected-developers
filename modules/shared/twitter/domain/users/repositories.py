from typing import Optional

from modules.shared.twitter.domain.users.entities import *
from modules.shared.twitter.domain.users.values import *

__all__ = ('UserRepository',)


class UserRepository:

    async def find_by_login(self, login: UserLogin) -> Optional[User]:
        raise NotImplementedError

    async def search_followed_users(self, user: User) -> Users:
        return await self.search_followed_users_by_id(user.id)

    async def search_followed_users_by_id(self, id: UserId) -> Users:
        raise NotImplementedError
