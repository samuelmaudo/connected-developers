from datetime import datetime
from typing import List

from pydantic import BaseModel


class ConnectedDevelopersResponse(BaseModel):
    connected: bool
    organisations: List[str]

    class Config:
        schema_extra = {
            'example': {
                'connected': True,
                'organisations': [
                    'org1',
                    'org2'
                ]
            }
        }


class NotConnectedDevelopersResponse(BaseModel):
    connected: bool

    class Config:
        schema_extra = {
            'example': {
                'connected': False
            }
        }


class NotExistingDeveloperResponse(BaseModel):
    errors: List[str]

    class Config:
        schema_extra = {
            'example': {
                'errors': [
                    'dev1 is not a valid user in github',
                    'dev1 is not a valid user in twitter',
                    'dev2 is not a valid user in twitter'
                ]
            }
        }


class TimedConnectedDevelopersResponse(BaseModel):
    registered_at: datetime
    connected: bool
    organisations: List[str]

    class Config:
        schema_extra = {
            'example': {
                'registered_at': '2021-10-30T13:54:45.485Z',
                'connected': True,
                'organisations': [
                    'org1',
                    'org2'
                ]
            }
        }


class TimedNotConnectedDevelopersResponse(BaseModel):
    registered_at: datetime
    connected: bool

    class Config:
        schema_extra = {
            'example': {
                'registered_at': '2021-10-30T13:54:45.485Z',
                'connected': False
            }
        }
