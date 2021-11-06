import pytest

from modules.shared.github.domain.users.entities import User
from modules.shared.github.domain.users.repositories import UserRepository
from modules.shared.github.domain.users.values import UserLogin


@pytest.mark.asyncio
async def test_finding_a_missing_user(github_user_repository: UserRepository):
    user = await github_user_repository.find_by_login(UserLogin('InmaculadaOjeda'))
    assert user is None


@pytest.mark.asyncio
async def test_finding_a_registered_user(github_user_repository: UserRepository):
    user = await github_user_repository.find_by_login(UserLogin('NayaraHidalgo'))
    assert user.login.value == 'NayaraHidalgo'


@pytest.mark.asyncio
async def test_user_not_having_any_organization(github_user_repository: UserRepository):
    user = User.from_primitives(132165146, 'JaimeSastre')
    orgs = await github_user_repository.search_organizations(user)
    assert not orgs


@pytest.mark.asyncio
async def test_user_having_some_organizations(github_user_repository: UserRepository):
    user = User.from_primitives(468749687, 'YoussefAriza')
    orgs = await github_user_repository.search_organizations(user)
    assert len(orgs) == 2
    assert orgs[0].login.value == 'Norset'
    assert orgs[1].login.value == 'Karmat'
