from datetime import datetime, timezone
from typing import List, Optional

from pydantic import BaseModel


class User(BaseModel):
    platform: str
    username: str
    exists: bool


class GitHubUser(User):

    def __init__(
        self,
        username: Optional[str] = None,
        exists: Optional[bool] = None,
        **data
    ) -> None:
        data['platform'] = 'github'

        if username is not None:
            data['username'] = username

        if exists is not None:
            data['exists'] = exists

        super().__init__(**data)


class TwitterUser(User):

    def __init__(
        self,
        username: Optional[str] = None,
        exists: Optional[bool] = None,
        **data
    ) -> None:
        data['platform'] = 'twitter'

        if username is not None:
            data['username'] = username

        if exists is not None:
            data['exists'] = exists

        super().__init__(**data)


class ConnectionCheck(BaseModel):
    registered_at: datetime
    connected: bool
    organisations: Optional[List[str]]

    def __init__(
        self,
        connected: Optional[bool] = None,
        organisations: Optional[List[str]] = None,
        **data
    ) -> None:
        if 'registered_at' not in data:
            data['registered_at'] = datetime.now(timezone.utc)

        if connected is not None:
            data['connected'] = connected

        if organisations is not None:
            data['organisations'] = organisations

        super().__init__(**data)
