from fastapi.responses import Response

from apps.api.rest.connected.responses import (
    ConnectedDevelopersResponse,
    NotConnectedDevelopersResponse,
    NotExistingDeveloperResponse,
    NotRegisteredDevelopersResponse,
    RegisteredDevelopersResponse
)
from modules.api.connected.application.services import (
    ConnectionChecker,
    ConnectionChecksSearcher
)
from modules.api.connected.domain.exceptions import UsersNotFound
from modules.api.connected.domain.values import CheckUser


class CheckConnectionController:

    def __init__(self, connection_checker: ConnectionChecker) -> None:
        self.connection_checker = connection_checker

    async def handle(self, login_1: str, login_2: str) -> Response:
        user_1 = CheckUser(login_1)
        user_2 = CheckUser(login_2)
        try:
            check = await self.connection_checker.check(user_1, user_2)
        except UsersNotFound as e:
            return NotExistingDeveloperResponse(e)

        if not check.organisations:
            return NotConnectedDevelopersResponse()

        return ConnectedDevelopersResponse(check.organisations)


class GetPreviousChecksController:

    def __init__(self, connection_checks_searcher: ConnectionChecksSearcher) -> None:
        self.connection_checks_searcher = connection_checks_searcher

    async def handle(self, login_1: str, login_2: str) -> Response:
        user_1 = CheckUser(login_1)
        user_2 = CheckUser(login_2)
        checks = await self.connection_checks_searcher.search(user_1, user_2)
        if checks:
            return RegisteredDevelopersResponse(checks)
        else:
            return NotRegisteredDevelopersResponse()
