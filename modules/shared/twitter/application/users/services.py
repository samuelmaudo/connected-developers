from modules.shared.twitter.domain.users.entities import *
from modules.shared.twitter.domain.users.exceptions import UserNotFound
from modules.shared.twitter.domain.users.repositories import UserRepository
from modules.shared.twitter.domain.users.values import *

__all__ = ('UserFinder', 'ConnectionChecker')


class UserFinder:

    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def find(self, login: UserLogin) -> User:
        user = await self.repository.find_by_login(login)
        if user is None:
            raise UserNotFound(login)

        return user


class ConnectionChecker:

    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def check(self, user_1: User, user_2: User) -> bool:
        if user_1 == user_2:
            return False

        followed_users = await self.repository.search_followed_users(user_1)
        if user_2 not in followed_users:
            return False

        followed_users = await self.repository.search_followed_users(user_2)
        if user_1 not in followed_users:
            return False

        return True
