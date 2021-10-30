import asyncio
from typing import Tuple

from fastapi.responses import Response

from api.connected.application.responses import (
    ConnectedDevelopersResponse,
    NotConnectedDevelopersResponse,
    NotExistingDeveloperResponse,
    NotRegisteredDevelopersResponse,
    RegisteredDevelopersResponse
)
from api.connected.domain.models import User
from api.connected.domain.services import (
    ConnectionChecksSearcher,
    ConnectionChecksStorer,
    GitHubConnectionChecker,
    GitHubUserFinder,
    TwitterConnectionChecker,
    TwitterUserFinder,
)


class CheckConnectionController:

    def __init__(self) -> None:
        self.twitter_user_finder = TwitterUserFinder()
        self.github_user_finder = GitHubUserFinder()
        self.twitter_connection_checker = TwitterConnectionChecker()
        self.github_connection_checker = GitHubConnectionChecker()
        self.connection_checks_storer = ConnectionChecksStorer()

    async def handle(self, username_1: str, username_2: str) -> Response:
        # noinspection PyTypeChecker
        users: Tuple[User] = await asyncio.gather(
            self.twitter_user_finder.find(username_1),
            self.twitter_user_finder.find(username_2),
            self.github_user_finder.find(username_1),
            self.github_user_finder.find(username_2),
        )
        errors = [
            f'{user.username} is not a valid user in {user.platform}'
            for user in users if not user.exists
        ]
        if errors:
            return NotExistingDeveloperResponse(errors)

        connected = await self.twitter_connection_checker.check(username_1, username_2)
        if not connected:
            await self.connection_checks_storer.store(False)
            return NotConnectedDevelopersResponse()

        organisations = await self.github_connection_checker.check(username_1, username_2)
        if not organisations:
            await self.connection_checks_storer.store(False)
            return NotConnectedDevelopersResponse()

        await self.connection_checks_storer.store(True, organisations)
        return ConnectedDevelopersResponse(organisations)


class GetPreviousChecksController:

    def __init__(self) -> None:
        self.connection_checks_searcher = ConnectionChecksSearcher()

    async def handle(self, username_1: str, username_2: str) -> Response:
        checks = await self.connection_checks_searcher.search(username_1, username_2)
        if not checks:
            return NotRegisteredDevelopersResponse()

        return RegisteredDevelopersResponse(checks)
