import pytest

from modules.shared.twitter.application.users.services import UserFinder, ConnectionChecker
from modules.shared.twitter.domain.users.entities import User
from modules.shared.twitter.domain.users.exceptions import UserNotFound
from modules.shared.twitter.domain.users.values import UserLogin


@pytest.mark.asyncio
async def test_finding_a_missing_user(twitter_user_finder: UserFinder):
    with pytest.raises(UserNotFound):
        await twitter_user_finder.find(UserLogin('InmaculadaOjeda'))


@pytest.mark.asyncio
async def test_finding_a_registered_user(twitter_user_finder: UserFinder):
    user = await twitter_user_finder.find(UserLogin('JaimeSastre'))
    assert user.login.value == 'JaimeSastre'


@pytest.mark.asyncio
async def test_checking_not_connected_users(twitter_connection_checker: ConnectionChecker):
    user_1 = User.from_primitives(132165146, 'CarmenAcosta')
    user_2 = User.from_primitives(468749687, 'JaimeSastre')
    assert not await twitter_connection_checker.check(user_1, user_2)


@pytest.mark.asyncio
async def test_checking_connected_users(twitter_connection_checker: ConnectionChecker):
    user_1 = User.from_primitives(736479749, 'YoussefAriza')
    user_2 = User.from_primitives(457936940, 'CandelaPazos')
    assert await twitter_connection_checker.check(user_1, user_2)
