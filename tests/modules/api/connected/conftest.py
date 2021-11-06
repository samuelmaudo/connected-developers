import pytest

from modules.api.connected.application.services import (
    ConnectionChecker,
    ConnectionCheckStorer,
    ConnectionChecksSearcher,
)
from modules.api.connected.infrastructure.repositories import (
    DummyConnectionCheckRepository,
)

from tests.modules.shared.github.users.conftest import *
from tests.modules.shared.twitter.users.conftest import *


__all__ = (
    'twitter_user_finder',
    'twitter_connection_checker',
    'github_user_finder',
    'github_connection_checker',
    'connection_checker',
    'connection_check_storer',
    'connection_checks_searcher',
    'connection_check_repository',
)


@pytest.fixture
def connection_check_repository():
    return DummyConnectionCheckRepository()


@pytest.fixture
def connection_check_storer(connection_check_repository):
    return ConnectionCheckStorer(connection_check_repository)


@pytest.fixture
def connection_checks_searcher(connection_check_repository):
    return ConnectionChecksSearcher(connection_check_repository)


@pytest.fixture
def connection_checker(
    twitter_user_finder,
    github_user_finder,
    twitter_connection_checker,
    github_connection_checker,
    connection_check_storer
):
    return ConnectionChecker(
        twitter_user_finder,
        github_user_finder,
        twitter_connection_checker,
        github_connection_checker,
        connection_check_storer
    )
