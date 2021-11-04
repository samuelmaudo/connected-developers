from modules.shared.kernel.domain.exceptions import AggregatedError, NotFoundError

__all__ = ('UsersNotFound',)


class UsersNotFound(AggregatedError[NotFoundError]):

    def error_code(self) -> str:
        return 'api_connected_users_not_found'

    def error_message(self) -> str:
        return 'Following users have not been found: {}'.format(
            ', '.join(f'<{error.key}>' for error in self.errors))
