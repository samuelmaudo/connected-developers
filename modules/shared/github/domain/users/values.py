from modules.shared.kernel.domain.values import Int, Str

__all__ = ('UserId', 'UserLogin', 'OrganizationId', 'OrganizationLogin')


class UserId(Int):
    ...


class UserLogin(Str):
    ...


class OrganizationId(Int):
    ...


class OrganizationLogin(Str):
    ...
