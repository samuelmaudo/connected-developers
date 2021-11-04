from dependency_injector import containers, providers

from modules.api.connected.application import services
from modules.api.connected.infrastructure import repositories

__all__ = ('ApiConnectedContainer',)


class ApiConnectedContainer(containers.DeclarativeContainer):

    _twitter_user_finder = providers.Dependency()
    _github_user_finder = providers.Dependency()
    _twitter_connection_checker = providers.Dependency()
    _github_connection_checker = providers.Dependency()

    connection_check_repository = providers.Factory(
        repositories.TortoiseConnectionCheckRepository
    )

    connection_check_storer = providers.Factory(
        services.ConnectionCheckStorer,
        connection_check_repository
    )
    connection_checks_searcher = providers.Factory(
        services.ConnectionChecksSearcher,
        connection_check_repository
    )
    connection_checker = providers.Factory(
        services.ConnectionChecker,
        _twitter_user_finder,
        _github_user_finder,
        _twitter_connection_checker,
        _github_connection_checker,
        connection_check_storer
    )
