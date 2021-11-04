from dependency_injector import containers, providers

from modules.shared.twitter.application.users import services
from modules.shared.twitter.infrastructure.users import repositories

__all__ = ('TwitterContainer',)


class TwitterContainer(containers.DeclarativeContainer):

    config = providers.Configuration(strict=True, ini_files=['config.ini'])

    user_repository = providers.Factory(
        repositories.ApiUserRepository,
        config.twitter.bearer_token
    )

    user_finder = providers.Factory(
        services.UserFinder,
        user_repository
    )
    connection_checker = providers.Factory(
        services.ConnectionChecker,
        user_repository
    )
