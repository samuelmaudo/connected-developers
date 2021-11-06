import pytest

from modules.api.connected.application.services import (
    ConnectionChecker,
    ConnectionChecksSearcher
)
from modules.api.connected.domain.exceptions import UsersNotFound
from modules.api.connected.domain.values import CheckUser


@pytest.mark.asyncio
async def test_checking_missing_users(connection_checker: ConnectionChecker):
    with pytest.raises(UsersNotFound):
        await connection_checker.check(CheckUser('NayaraHidalgo'), CheckUser('InmaculadaOjeda'))


@pytest.mark.asyncio
async def test_checking_not_connected_users(connection_checker: ConnectionChecker):
    check = await connection_checker.check(CheckUser('CandelaPazos'), CheckUser('JaimeSastre'))
    assert not check.organisations


@pytest.mark.asyncio
async def test_checking_connected_users(connection_checker: ConnectionChecker):
    check = await connection_checker.check(CheckUser('YoussefAriza'), CheckUser('CandelaPazos'))
    assert len(check.organisations) >= 1


@pytest.mark.asyncio
async def test_searching_missing_connection_checks(connection_checks_searcher: ConnectionChecksSearcher):
    checks = await connection_checks_searcher.search(CheckUser('NayaraHidalgo'), CheckUser('InmaculadaOjeda'))
    assert not checks


@pytest.mark.asyncio
async def test_searching_not_connected_connection_checks(connection_checks_searcher: ConnectionChecksSearcher):
    checks = await connection_checks_searcher.search(CheckUser('CandelaPazos'), CheckUser('JaimeSastre'))
    assert len(checks) == 1
    assert not checks[0].organisations


@pytest.mark.asyncio
async def test_searching_connected_connection_checks(connection_checks_searcher: ConnectionChecksSearcher):
    checks = await connection_checks_searcher.search(CheckUser('YoussefAriza'), CheckUser('CandelaPazos'))
    assert len(checks) == 1
    assert len(checks[0].organisations) >= 1
