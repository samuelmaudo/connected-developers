import pytest

from modules.shared.twitter.domain.users.entities import User
from modules.shared.twitter.domain.users.repositories import UserRepository
from modules.shared.twitter.domain.users.values import UserLogin


@pytest.mark.asyncio
async def test_finding_a_missing_user(twitter_user_repository: UserRepository):
    user = await twitter_user_repository.find_by_login(UserLogin('InmaculadaOjeda'))
    assert user is None


@pytest.mark.asyncio
async def test_finding_a_registered_user(twitter_user_repository: UserRepository):
    user = await twitter_user_repository.find_by_login(UserLogin('JaimeSastre'))
    assert user.login.value == 'JaimeSastre'


@pytest.mark.asyncio
async def test_user_not_following_any_user(twitter_user_repository: UserRepository):
    user = User.from_primitives(132165146, 'CarmenAcosta')
    followed_users = await twitter_user_repository.search_followed_users(user)
    assert not followed_users


@pytest.mark.asyncio
async def test_user_following_other_users(twitter_user_repository: UserRepository):
    user = User.from_primitives(468749687, 'JaimeSastre')
    followed_users = await twitter_user_repository.search_followed_users(user)
    assert len(followed_users) == 2
    assert followed_users[0].login.value == 'AbelCid'
    assert followed_users[1].login.value == 'CarmenAcosta'
