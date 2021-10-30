from typing import List

from fastapi.responses import JSONResponse, Response

from api.connected.domain.models import ConnectionCheck


class ConnectedDevelopersResponse(JSONResponse):

    def __init__(self, organisations: List[str]) -> None:
        super().__init__(
            status_code=200,
            content={
                'connected': True,
                'organisations': organisations
            })


class NotConnectedDevelopersResponse(JSONResponse):

    def __init__(self) -> None:
        super().__init__(
            status_code=404,
            content={
                'connected': False
            })


class NotExistingDeveloperResponse(JSONResponse):

    def __init__(self, errors: List[str]) -> None:
        super().__init__(
            status_code=400,
            content={
                'errors': errors
            })


class RegisteredDevelopersResponse(JSONResponse):

    def __init__(self, checks: List[ConnectionCheck]) -> None:
        super().__init__(
            status_code=200,
            content=[
                check.dict()
                for check
                in checks
            ])


class NotRegisteredDevelopersResponse(Response):

    def __init__(self) -> None:
        super().__init__(status_code=404)
