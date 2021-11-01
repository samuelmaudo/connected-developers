from fastapi.responses import JSONResponse, Response

from modules.api.connected.domain.entities import ConnectionChecks
from modules.api.connected.domain.exceptions import UsersNotFound
from modules.api.connected.domain.values import CheckOrganisations

__all__ = (
    'ConnectedDevelopersResponse',
    'NotConnectedDevelopersResponse',
    'NotExistingDeveloperResponse',
    'RegisteredDevelopersResponse',
    'NotRegisteredDevelopersResponse'
)


class ConnectedDevelopersResponse(JSONResponse):

    def __init__(self, organisations: CheckOrganisations) -> None:
        super().__init__(
            status_code=200,
            content={
                'connected': True,
                'organisations': [
                    organisation.value
                    for organisation
                    in organisations
                ]
            })


class NotConnectedDevelopersResponse(JSONResponse):

    def __init__(self) -> None:
        super().__init__(
            status_code=404,
            content={
                'connected': False
            })


class NotExistingDeveloperResponse(JSONResponse):

    def __init__(self, err: UsersNotFound) -> None:
        super().__init__(
            status_code=400,
            content={
                'errors': [
                    '{} is not a valid user in {}'.format(
                        error.key,
                        'twitter' if 'twitter' in error.error_code() else 'github'
                    )
                    for error
                    in err.errors
                ]
            })


class RegisteredDevelopersResponse(JSONResponse):

    def __init__(self, checks: ConnectionChecks) -> None:
        data = []
        for check in checks:
            item = {
                'registered_at': check.registered_at.value,
                'connected': check.connected.value
            }
            if check.organisations:
                item['organisations'] = [
                    organisation.value
                    for organisation
                    in check.organisations
                ]

            data.append(item)

        super().__init__(status_code=200, content=data)


class NotRegisteredDevelopersResponse(Response):

    def __init__(self) -> None:
        super().__init__(status_code=404)
