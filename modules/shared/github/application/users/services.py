import asyncio
from typing import Tuple

from modules.shared.github.domain.users.entities import *
from modules.shared.github.domain.users.exceptions import UserNotFound
from modules.shared.github.domain.users.repositories import UserRepository
from modules.shared.github.domain.users.values import *

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

    async def check(self, user_1: User, user_2: User) -> Organizations:
        if user_1 == user_2:
            return Organizations()

        # noinspection PyTypeChecker
        organisations: Tuple[Organizations, Organizations] = await asyncio.gather(
            self.repository.search_organizations(user_1),
            self.repository.search_organizations(user_2)
        )

        return Organizations(set(organisations[0]) & set(organisations[1]))
