from typing import List, Union

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Path
from fastapi.responses import Response

from apps.api.rest.connected.controllers import (
    CheckConnectionController,
    GetPreviousChecksController
)
from apps.api.rest.connected.models import (
    ConnectedDevelopersResponse,
    NotConnectedDevelopersResponse,
    NotExistingDeveloperResponse,
    TimedConnectedDevelopersResponse,
    TimedNotConnectedDevelopersResponse
)
from modules.api.connected.application.services import (
    ConnectionChecker,
    ConnectionChecksSearcher
)

router = APIRouter(
    prefix='/connected',
    tags=['connected'],
)


@router.get(
    '/realtime/{dev1}/{dev2}',
    summary='Check if two developers are connected and what GitHub organisations they have in common.',
    responses={
        200: {
            'description': 'Case they are connected',
            'model': ConnectedDevelopersResponse
        },
        400: {
            'description': 'Case any of them does not exists',
            'model': NotExistingDeveloperResponse
        },
        404: {
            'description': 'Case they are not connected',
            'model': NotConnectedDevelopersResponse
        }
    }
)
@inject
async def check_connection(
    dev1: str = Path(..., description='Account of the first developer'),
    dev2: str = Path(..., description='Account of the second developer'),
    connection_checker: ConnectionChecker = Depends(Provide['connected.connection_checker'])
) -> Response:
    return await CheckConnectionController(connection_checker).handle(dev1, dev2)


@router.get(
    '/register/{dev1}/{dev2}',
    summary='This endpoint will return all the related information from previous requests to the real-time endpoint.',
    responses={
        200: {
            'description': 'Case they have been registered through the realtime endpoint',
            'model': List[Union[TimedConnectedDevelopersResponse, TimedNotConnectedDevelopersResponse]]
        },
        404: {
            'description': 'Case they are not registered',
            'model': None
        }
    }
)
@inject
async def get_previous_checks(
    dev1: str = Path(..., description='Account of the first developer'),
    dev2: str = Path(..., description='Account of the second developer'),
    connection_checks_searcher: ConnectionChecksSearcher = Depends(Provide['connected.connection_checks_searcher'])
) -> Response:
    return await GetPreviousChecksController(connection_checks_searcher).handle(dev1, dev2)
