import pytest

from modules.shared.kernel.domain.collections import Collection


class StringCollection(Collection[str]):

    def type(self):
        return str


coll = StringCollection(['a', 'b', 'c'])


# noinspection PyTypeChecker
@pytest.mark.asyncio
async def test_validation():
    with pytest.raises(TypeError):
        StringCollection([1, 2, 3])


@pytest.mark.asyncio
async def test_representation():
    assert repr(coll) == "StringCollection('a', 'b', 'c')"


@pytest.mark.asyncio
async def test_length():
    assert len(coll) == 3


@pytest.mark.asyncio
async def test_iteration():
    assert list(coll) == ['a', 'b', 'c']


@pytest.mark.asyncio
async def test_reverse_iteration():
    assert list(reversed(coll)) == ['c', 'b', 'a']


@pytest.mark.asyncio
async def test_containment():
    assert 'b' in coll
    assert 'x' not in coll
