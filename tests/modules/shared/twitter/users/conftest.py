import pytest

from modules.shared.twitter.application.users.services import ConnectionChecker, UserFinder
from modules.shared.twitter.domain.users.repositories import UserRepository
from modules.shared.twitter.infrastructure.users.repositories import DummyUserRepository

__all__ = ('twitter_user_finder', 'twitter_connection_checker', 'twitter_user_repository')


@pytest.fixture
def twitter_user_repository():
    return DummyUserRepository()


@pytest.fixture
def twitter_user_finder(twitter_user_repository: UserRepository):
    return UserFinder(twitter_user_repository)


@pytest.fixture
def twitter_connection_checker(twitter_user_repository: UserRepository):
    return ConnectionChecker(twitter_user_repository)
