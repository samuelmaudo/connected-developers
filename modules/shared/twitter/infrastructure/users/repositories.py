from typing import Any, Dict, List, Optional, Tuple

import orjson
from httpx import AsyncClient, Response

from modules.shared.twitter.domain.users.entities import *
from modules.shared.twitter.domain.users.repositories import *
from modules.shared.twitter.domain.users.values import *

__all__ = ('ApiUserRepository', 'DummyUserRepository')


class ApiUserRepository(UserRepository):

    def __init__(self, bearer_token: str) -> None:
        self.bearer_token: str = bearer_token

    async def find_by_login(self, login: UserLogin) -> Optional[User]:
        async with self._get_api_client() as client:
            response: Response = await client.get(f'/2/users/by/username/{login}')

        if response.status_code != 200:
            return None

        content = orjson.loads(response.content)
        if 'errors' in content or 'data' not in content:
            return None

        return self._make_user(content['data'])

    async def search_followed_users_by_id(self, id: UserId) -> Users:
        async with self._get_api_client() as client:
            users: List[User] = []
            pagination_token = None
            while True:

                params: Dict[str, str] = {}
                if pagination_token is not None:
                    params['pagination_token'] = pagination_token

                response: Response = await client.get(
                    f'/2/users/{id}/following',
                    params=params)

                if response.status_code != 200:
                    return Users(users)

                content = orjson.loads(response.content)
                if 'errors' in content or 'data' not in content:
                    return Users(users)

                users.extend(self._make_user(data) for data in content['data'])

                if 'meta' in content and 'next_token' in content['meta']:
                    pagination_token = content['meta']['next_token']
                else:
                    return Users(users)

    def _get_api_client(self) -> AsyncClient:
        return AsyncClient(
            base_url='https://api.twitter.com',
            headers={'Authorization': f'Bearer {self.bearer_token}'})

    def _make_user(self, data: Dict[str, Any]) -> User:
        return User.from_primitives(data['id'], data['username'])


class DummyUserRepository(UserRepository):

    _users: Dict[str, Tuple[int, str]] = {
        'JaimeSastre': (468749687, 'JaimeSastre'),
        'YoussefAriza': (736479749, 'YoussefAriza'),
        'CarmenAcosta': (132165146, 'CarmenAcosta'),
        'CandelaPazos': (457936940, 'CandelaPazos'),
    }
    _followings: Dict[int, List[Tuple[int, str]]] = {
        468749687: [
            (874943489, 'AbelCid'),
            (132165146, 'CarmenAcosta')
        ],
        736479749: [
            (457936940, 'CandelaPazos')
        ],
        132165146: [],
        457936940: [
            (736479749, 'YoussefAriza')
        ],
    }

    async def find_by_login(self, login: UserLogin) -> Optional[User]:
        if login.value not in self._users:
            return None

        return User.from_primitives(*self._users[login.value])

    async def search_followed_users_by_id(self, id: UserId) -> Users:
        if id.value not in self._followings:
            return Users()

        return Users(
            User.from_primitives(*following)
            for following
            in self._followings[id.value]
        )
