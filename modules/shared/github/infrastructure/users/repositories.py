from typing import Any, Dict, Optional

import orjson
from httpx import AsyncClient, Response

from modules.shared.github.domain.users.entities import *
from modules.shared.github.domain.users.repositories import *
from modules.shared.github.domain.users.values import *

__all__ = ('ApiUserRepository',)


class ApiUserRepository(UserRepository):

    def __init__(self, login: str, personal_access_token: str) -> None:
        self.login = login
        self.personal_access_token = personal_access_token

    async def find_by_login(self, login: UserLogin) -> Optional[User]:
        async with self._get_api_client() as client:
            response: Response = await client.get(f'/users/{login}')

        if response.status_code != 200:
            return None

        return self._make_user(orjson.loads(response.content))

    async def search_organizations_by_login(self, login: UserLogin) -> Organizations:
        async with self._get_api_client() as client:
            orgs = []
            url = f'/users/{login}/orgs?page=1'
            while True:

                response: Response = await client.get(url)

                if response.status_code != 200:
                    return Organizations(orgs)

                content = orjson.loads(response.content)
                orgs.extend(self._make_organization(data) for data in content)

                links = response.links
                if 'next' in links and 'url' in links['next']:
                    url = links['next']['url']
                else:
                    return Organizations(orgs)

    def _get_api_client(self) -> AsyncClient:
        return AsyncClient(
            base_url='https://api.github.com',
            auth=(self.login, self.personal_access_token))

    def _make_organization(self, data: Dict[str, Any]) -> Organization:
        return Organization.from_primitives(data['id'], data['login'])

    def _make_user(self, data: Dict[str, Any]) -> User:
        return User.from_primitives(data['id'], data['login'])
