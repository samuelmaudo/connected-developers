import os
from typing import Dict, Optional

from httpx import AsyncClient, Response

from modules.shared.github.domain.users.entities import *
from modules.shared.github.domain.users.repositories import *
from modules.shared.github.domain.users.values import *

__all__ = ('ApiUserRepository',)


class ApiUserRepository(UserRepository):

    def __init__(self) -> None:
        self.login = os.getenv('GITHUB_USERNAME')
        self.personal_access_token = os.getenv('GITHUB_PERSONAL_ACCESS_TOKEN')

    async def find_by_login(self, login: UserLogin) -> Optional[User]:
        async with self._get_api_client() as client:
            response: Response = await client.get(f'/users/{login}')

        if response.status_code != 200:
            return None

        return self._make_user(response.json())

    async def search_organizations_by_login(self, login: UserLogin) -> Organizations:
        async with self._get_api_client() as client:
            response: Response = await client.get(f'/users/{login}/orgs')

        if response.status_code != 200:
            return Organizations()

        return Organizations(self._make_organization(data) for data in response.json())

    def _get_api_client(self) -> AsyncClient:
        return AsyncClient(
            base_url='https://api.github.com',
            auth=(self.login, self.personal_access_token))

    def _make_organization(self, data: Dict) -> Organization:
        return Organization.from_primitives(data['id'], data['login'])

    def _make_user(self, data: Dict) -> User:
        return User.from_primitives(data['id'], data['login'])
