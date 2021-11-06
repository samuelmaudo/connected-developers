import pytest

from modules.shared.github.application.users.services import UserFinder, ConnectionChecker
from modules.shared.github.domain.users.entities import User
from modules.shared.github.domain.users.exceptions import UserNotFound
from modules.shared.github.domain.users.values import UserLogin


@pytest.mark.asyncio
async def test_finding_a_missing_user(github_user_finder: UserFinder):
    with pytest.raises(UserNotFound):
        await github_user_finder.find(UserLogin('InmaculadaOjeda'))


@pytest.mark.asyncio
async def test_finding_a_registered_user(github_user_finder: UserFinder):
    user = await github_user_finder.find(UserLogin('JaimeSastre'))
    assert user.login.value == 'JaimeSastre'


@pytest.mark.asyncio
async def test_checking_not_connected_users(github_connection_checker: ConnectionChecker):
    user_1 = User.from_primitives(385468548, 'JaimeSastre')
    user_2 = User.from_primitives(288456873, 'NayaraHidalgo')
    assert not await github_connection_checker.check(user_1, user_2)


@pytest.mark.asyncio
async def test_checking_connected_users(github_connection_checker: ConnectionChecker):
    user_1 = User.from_primitives(854722154, 'YoussefAriza')
    user_2 = User.from_primitives(541876158, 'CandelaPazos')
    assert await github_connection_checker.check(user_1, user_2)
