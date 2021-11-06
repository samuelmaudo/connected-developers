import pytest

from modules.shared.github.application.users.services import ConnectionChecker, UserFinder
from modules.shared.github.domain.users.repositories import UserRepository
from modules.shared.github.infrastructure.users.repositories import DummyUserRepository

__all__ = ('github_user_finder', 'github_connection_checker', 'github_user_repository')


@pytest.fixture
def github_user_repository():
    return DummyUserRepository()


@pytest.fixture
def github_user_finder(github_user_repository: UserRepository):
    return UserFinder(github_user_repository)


@pytest.fixture
def github_connection_checker(github_user_repository: UserRepository):
    return ConnectionChecker(github_user_repository)
