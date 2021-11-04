from dependency_injector import containers, providers

from modules.shared.github.application.users import services
from modules.shared.github.infrastructure.users import repositories

__all__ = ('GitHubContainer',)


class GitHubContainer(containers.DeclarativeContainer):

    config = providers.Configuration(strict=True, ini_files=['config.ini'])

    user_repository = providers.Factory(
        repositories.ApiUserRepository,
        config.github.login,
        config.github.personal_access_token
    )

    user_finder = providers.Factory(
        services.UserFinder,
        user_repository
    )
    connection_checker = providers.Factory(
        services.ConnectionChecker,
        user_repository
    )
