from dataclasses import FrozenInstanceError
from datetime import datetime

import pytest
from pydantic import ValidationError

from modules.shared.kernel.domain.values import *


# noinspection PyDataclass
@pytest.mark.asyncio
async def test_value_immutability():
    val = Value(1)
    with pytest.raises(FrozenInstanceError):
        val.value = 0


@pytest.mark.asyncio
async def test_value_representation():
    assert repr(Value(b'abc')) == "Value(b'abc')"


# noinspection PyTypeChecker
@pytest.mark.asyncio
async def test_bool_validation():
    assert Bool(True).value is True
    assert Bool(False).value is False
    assert Bool(1).value is True
    assert Bool(0).value is False
    assert Bool('on').value is True
    assert Bool('off').value is False
    with pytest.raises(ValidationError):
        Bool(10)
    with pytest.raises(ValidationError):
        Bool('ABC')
    with pytest.raises(ValidationError):
        Bool([])
    with pytest.raises(ValidationError):
        Bool(None)


# noinspection PyTypeChecker
@pytest.mark.asyncio
async def test_bool_conversion_to_string():
    assert str(Bool(True)) == 'true'
    assert str(Bool(False)) == 'false'
    assert str(Bool(1)) == 'true'
    assert str(Bool(0)) == 'false'
    assert str(Bool('on')) == 'true'
    assert str(Bool('off')) == 'false'


# noinspection PyTypeChecker
@pytest.mark.asyncio
async def test_datetime_validation():
    assert isinstance(DateTime(datetime(2021, 11, 6, 2, 23, 00)).value, datetime)
    assert isinstance(DateTime(1636161780).value, datetime)
    assert isinstance(DateTime(1636161780.553146).value, datetime)
    assert isinstance(DateTime('2021-11-06T2:23:00').value, datetime)
    assert isinstance(DateTime('1636161780').value, datetime)
    assert isinstance(DateTime('1636161780.553146').value, datetime)
    with pytest.raises(ValidationError):
        DateTime('ABC')
    with pytest.raises(ValidationError):
        DateTime([])
    with pytest.raises(ValidationError):
        DateTime(None)


# noinspection PyTypeChecker
@pytest.mark.asyncio
async def test_datetime_conversion_to_string():
    assert str(DateTime(datetime(2021, 11, 6, 2, 23, 00))) == '2021-11-06T02:23:00'
    assert str(DateTime(1636161780)) == '2021-11-06T01:23:00+00:00'
    assert str(DateTime(1636161780.553146)) == '2021-11-06T01:23:00.553146+00:00'
    assert str(DateTime('2021-11-06T2:23:00')) == '2021-11-06T02:23:00'
    assert str(DateTime('1636161780')) == '2021-11-06T01:23:00+00:00'
    assert str(DateTime('1636161780.553146')) == '2021-11-06T01:23:00.553146+00:00'


# noinspection PyTypeChecker
@pytest.mark.asyncio
async def test_int_validation():
    assert isinstance(Int(0).value, int)
    assert isinstance(Int(1).value, int)
    assert isinstance(Int(1.0).value, int)
    assert isinstance(Int(True).value, int)
    assert isinstance(Int('1').value, int)
    with pytest.raises(ValidationError):
        Int('ABC')
    with pytest.raises(ValidationError):
        Int([])
    with pytest.raises(ValidationError):
        Int(None)


# noinspection PyTypeChecker
@pytest.mark.asyncio
async def test_int_conversion_to_string():
    assert str(Int(0)) == '0'
    assert str(Int(1)) == '1'
    assert str(Int(1.0)) == '1'
    assert str(Int(True)) == '1'
    assert str(Int('1')) == '1'


# noinspection PyTypeChecker
@pytest.mark.asyncio
async def test_str_validation():
    assert isinstance(Str('').value, str)
    assert isinstance(Str('ABC').value, str)
    assert isinstance(Str(1).value, str)
    assert isinstance(Str(b'abc').value, str)
    with pytest.raises(ValidationError):
        Str([])
    with pytest.raises(ValidationError):
        Str(None)


# noinspection PyTypeChecker
@pytest.mark.asyncio
async def test_str_conversion_to_string():
    assert str(Str('')) == ''
    assert str(Str('ABC')) == 'ABC'
    assert str(Str(1)) == '1'
    assert str(Str(b'abc')) == 'abc'


# noinspection PyTypeChecker
@pytest.mark.asyncio
async def test_uuid_validation():
    assert isinstance(Uuid('123e4567-e89b-12d3-a456-426614174000').value, str)
    assert isinstance(Uuid(b'123e4567-e89b-12d3-a456-426614174000').value, str)
    assert isinstance(Uuid('{123e4567-e89b-12d3-a456-426652340000}').value, str)
    assert isinstance(Uuid('urn:uuid:123e4567-e89b-12d3-a456-426655440000').value, str)
    with pytest.raises(ValidationError):
        Uuid('')
    with pytest.raises(ValidationError):
        Uuid('ABC')
    with pytest.raises(ValidationError):
        Uuid(None)


# noinspection PyTypeChecker
@pytest.mark.asyncio
async def test_uuid_conversion_to_string():
    assert str(Uuid('123e4567-e89b-12d3-a456-426614174000')) == '123e4567-e89b-12d3-a456-426614174000'
    assert str(Uuid(b'123e4567-e89b-12d3-a456-426614174000')) == '123e4567-e89b-12d3-a456-426614174000'
    assert str(Uuid('{123e4567-e89b-12d3-a456-426652340000}')) == '{123e4567-e89b-12d3-a456-426652340000}'
    assert str(Uuid('urn:uuid:123e4567-e89b-12d3-a456-426655440000')) == 'urn:uuid:123e4567-e89b-12d3-a456-426655440000'
