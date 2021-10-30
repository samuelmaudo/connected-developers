from typing import List, Union

from fastapi import APIRouter, Path
from fastapi.responses import Response

from api.connected.application.controllers import (
    CheckConnectionController,
    GetPreviousChecksController
)
from api.connected.application.models import (
    ConnectedDevelopersResponse,
    NotConnectedDevelopersResponse,
    NotExistingDeveloperResponse,
    TimedConnectedDevelopersResponse,
    TimedNotConnectedDevelopersResponse
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
async def check_connection(
    dev1: str = Path(..., description='Account of the first developer'),
    dev2: str = Path(..., description='Account of the second developer')
) -> Response:
    return await CheckConnectionController().handle(dev1, dev2)


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
async def get_previous_checks(
    dev1: str = Path(..., description='Account of the first developer'),
    dev2: str = Path(..., description='Account of the second developer')
) -> Response:
    return await GetPreviousChecksController().handle(dev1, dev2)
