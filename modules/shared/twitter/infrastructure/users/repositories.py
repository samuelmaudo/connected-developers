import os
from typing import Dict, Optional

from httpx import AsyncClient, Response

from modules.shared.twitter.domain.users.entities import *
from modules.shared.twitter.domain.users.repositories import *
from modules.shared.twitter.domain.users.values import *

__all__ = ('ApiUserRepository',)


class ApiUserRepository(UserRepository):

    def __init__(self) -> None:
        self.bearer_token = os.getenv('TWITTER_BEARER_TOKEN')

    async def find_by_login(self, login: UserLogin) -> Optional[User]:
        async with self._get_api_client() as client:
            response: Response = await client.get(f'/2/users/by/username/{login}')

        if response.status_code != 200:
            return None

        content = response.json()
        if 'errors' in content or 'data' not in content:
            return None

        return self._make_user(content['data'])

    async def search_followed_users_by_id(self, id: UserId) -> Users:
        async with self._get_api_client() as client:
            response: Response = await client.get(f'/2/users/{id}/following')

        if response.status_code != 200:
            return Users()

        content = response.json()
        if 'errors' in content or 'data' not in content:
            return Users()

        return Users(self._make_user(data) for data in content['data'])

    def _get_api_client(self) -> AsyncClient:
        return AsyncClient(
            base_url='https://api.twitter.com',
            headers={'Authorization': f'Bearer {self.bearer_token}'})

    def _make_user(self, data: Dict) -> User:
        return User.from_primitives(data['id'], data['username'])
