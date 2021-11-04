from dependency_injector import containers, providers

__all__ = ('ApiContainer',)

from modules.api.connected.infrastructure.containers import ApiConnectedContainer
from modules.shared.github.infrastructure.shared.containers import GitHubContainer
from modules.shared.kernel.infrastructure.containers import KernelContainer
from modules.shared.twitter.infrastructure.shared.containers import TwitterContainer


class ApiContainer(containers.DeclarativeContainer):

    kernel = providers.Container(KernelContainer)
    twitter = providers.Container(TwitterContainer)
    github = providers.Container(GitHubContainer)

    connected = providers.Container(
        ApiConnectedContainer,
        _twitter_user_finder=twitter.user_finder,
        _github_user_finder=github.user_finder,
        _twitter_connection_checker=twitter.connection_checker,
        _github_connection_checker=github.connection_checker,
    )

    tortoise_modules = providers.Object([
        'modules.api.connected.infrastructure.repositories',
    ])
