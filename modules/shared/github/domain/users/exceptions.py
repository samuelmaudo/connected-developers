from modules.shared.kernel.domain.exceptions import NotFoundError
from modules.shared.github.domain.users.values import UserLogin

__all__ = ('UserNotFound',)


class UserNotFound(NotFoundError[UserLogin]):

    def error_code(self) -> str:
        return 'github_user_not_found'

    def error_message(self) -> str:
        return f'GitHub user <{self._key}> has not been found'
