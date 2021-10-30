from typing import List, Optional

from api import settings
from api.connected.domain.models import (
    ConnectionCheck,
    GitHubUser,
    TwitterUser,
    User
)


class TwitterUserFinder:

    def __init__(self) -> None:
        self.bearer_token = settings.TWITTER_BEARER_TOKEN

    async def find(self, username: str) -> User:
        return TwitterUser(username, False)


class GitHubUserFinder:

    def __init__(self) -> None:
        self.personal_access_token = settings.GITHUB_PERSONAL_ACCESS_TOKEN

    async def find(self, username: str) -> User:
        return GitHubUser(username, False)


class TwitterConnectionChecker:

    def __init__(self) -> None:
        self.bearer_token = settings.TWITTER_BEARER_TOKEN

    async def check(self, username_1: str, username_2: str) -> bool:
        return False


class GitHubConnectionChecker:

    def __init__(self) -> None:
        self.personal_access_token = settings.GITHUB_PERSONAL_ACCESS_TOKEN

    async def check(self, username_1: str, username_2: str) -> List[str]:
        return []


class ConnectionChecksStorer:

    async def store(self, connected: bool, organisations: Optional[List[str]] = None) -> ConnectionCheck:
        return ConnectionCheck(connected, organisations)


class ConnectionChecksSearcher:

    async def search(self, username_1: str, username_2: str) -> List[ConnectionCheck]:
        return []
