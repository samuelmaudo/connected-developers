import asyncio
from datetime import datetime, timezone
from typing import List, Optional, Union

from modules.api.connected.domain.entities import *
from modules.api.connected.domain.exceptions import *
from modules.api.connected.domain.values import *
from modules.api.connected.infrastructure.repositories import *
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


class ConnectionChecker:

    def __init__(self) -> None:
        self.twitter_user_finder = TwitterUserFinder()
        self.github_user_finder = GitHubUserFinder()
        self.twitter_connection_checker = TwitterConnectionChecker()
        self.github_connection_checker = GitHubConnectionChecker()
        self.connection_checks_storer = ConnectionCheckStorer()

    async def check(self, user_1: CheckUser, user_2: CheckUser):
        tasks = [
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
            return await self.connection_checks_storer.store(user_1, user_2)

        organizations = await self.github_connection_checker.check(*github_users)
        if not organizations:
            return await self.connection_checks_storer.store(user_1, user_2)

        organisations = CheckOrganisations(
            CheckOrganisation(organization.login.value)
            for organization
            in organizations
        )
        return await self.connection_checks_storer.store(user_1, user_2, organisations)


class ConnectionCheckStorer:

    def __init__(self) -> None:
        self.repository = TortoiseConnectionCheckRepository()

    async def store(
        self,
        user_1: CheckUser,
        user_2: CheckUser,
        organisations: Optional[CheckOrganisations] = None,
        id: Optional[CheckId] = None,
        registered_at: Optional[CheckRegistrationDateTime] = None
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

    def __init__(self) -> None:
        self.repository = TortoiseConnectionCheckRepository()

    async def search(self, user_1: CheckUser, user_2: CheckUser) -> ConnectionChecks:
        if user_1 == user_2:
            return ConnectionChecks()

        return await self.repository.search_by_users(user_1, user_2)
