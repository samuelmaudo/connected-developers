import asyncio
from datetime import datetime, timezone
from typing import Awaitable, List, Union

from modules.api.connected.domain.entities import *
from modules.api.connected.domain.exceptions import *
from modules.api.connected.domain.repositories import *
from modules.api.connected.domain.values import *
from modules.shared.github.application.users.services import (
    ConnectionChecker as GitHubConnectionChecker,
    UserFinder as GitHubUserFinder,
)
from modules.shared.github.domain.users.entities import User as GitHubUser
from modules.shared.github.domain.users.exceptions import UserNotFound as GitHubUserNotFound
from modules.shared.github.domain.users.values import UserLogin as GitHubUserLogin
from modules.shared.twitter.application.users.services import (
    ConnectionChecker as TwitterConnectionChecker,
    UserFinder as TwitterUserFinder,
)
from modules.shared.twitter.domain.users.entities import User as TwitterUser
from modules.shared.twitter.domain.users.exceptions import UserNotFound as TwitterUserNotFound
from modules.shared.twitter.domain.users.values import UserLogin as TwitterUserLogin

__all__ = ('ConnectionChecker', 'ConnectionCheckStorer', 'ConnectionChecksSearcher')


class ConnectionCheckStorer:

    def __init__(self, repository: ConnectionCheckRepository) -> None:
        self.repository = repository

    async def store(
        self,
        user_1: CheckUser,
        user_2: CheckUser,
        organisations: CheckOrganisations = None,
        id: CheckId = None,
        registered_at: CheckRegistrationDateTime = None
    ) -> ConnectionCheck:
        if id is None:
            id = CheckId.random()

        if registered_at is None:
            registered_at = CheckRegistrationDateTime(datetime.now(timezone.utc))

        if organisations is None:
            organisations = CheckOrganisations()

        check = ConnectionCheck.store(id, registered_at, user_1, user_2, organisations)
        await self.repository.save(check)
        return check


class ConnectionChecksSearcher:

    def __init__(self, repository: ConnectionCheckRepository) -> None:
        self.repository = repository

    async def search(self, user_1: CheckUser, user_2: CheckUser) -> ConnectionChecks:
        if user_1 == user_2:
            return ConnectionChecks()

        return await self.repository.search_by_users(user_1, user_2)


class ConnectionChecker:

    def __init__(
        self,
        twitter_user_finder: TwitterUserFinder,
        github_user_finder: GitHubUserFinder,
        twitter_connection_checker: TwitterConnectionChecker,
        github_connection_checker: GitHubConnectionChecker,
        connection_check_storer: ConnectionCheckStorer
    ) -> None:
        self.twitter_user_finder = twitter_user_finder
        self.github_user_finder = github_user_finder
        self.twitter_connection_checker = twitter_connection_checker
        self.github_connection_checker = github_connection_checker
        self.connection_check_storer = connection_check_storer

    async def check(self, user_1: CheckUser, user_2: CheckUser) -> ConnectionCheck:
        tasks: List[Awaitable[Union[TwitterUser, GitHubUser]]] = [
            self.twitter_user_finder.find(TwitterUserLogin(user_1.value)),
            self.twitter_user_finder.find(TwitterUserLogin(user_2.value)),
            self.github_user_finder.find(GitHubUserLogin(user_1.value)),
            self.github_user_finder.find(GitHubUserLogin(user_2.value)),
        ]
        users: List[Union[TwitterUser, GitHubUser]] = []
        errors: List[Union[TwitterUserNotFound, GitHubUserNotFound]] = []
        for task in asyncio.as_completed(tasks):
            try:
                users.append(await task)
            except (TwitterUserNotFound, GitHubUserNotFound) as e:
                errors.append(e)

        if errors:
            raise UsersNotFound(errors)

        twitter_users: List[TwitterUser] = []
        github_users: List[GitHubUser] = []
        for user in users:
            if isinstance(user, TwitterUser):
                twitter_users.append(user)
            else:
                github_users.append(user)

        connected = await self.twitter_connection_checker.check(*twitter_users)
        if not connected:
            return await self.connection_check_storer.store(user_1, user_2)

        organizations = await self.github_connection_checker.check(*github_users)
        if not organizations:
            return await self.connection_check_storer.store(user_1, user_2)

        organisations = CheckOrganisations(
            CheckOrganisation(organization.login.value)
            for organization
            in organizations
        )
        return await self.connection_check_storer.store(user_1, user_2, organisations)
