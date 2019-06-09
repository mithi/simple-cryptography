import pytest
from paddingoracle import PaddingOracle, decode

@pytest.fixture
def set1():
    t = 'http://crypto-class.appspot.com/po?er='
    c = "f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4"
    m = "The Magic Words are Squeamish Ossifrage"
    return t, c, m

@pytest.fixture
def set2():
    t = "http://localhost:9000/po?er="
    c = "4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81"
    m = "Basic CBC mode encryption needs padding."
    return t, c, m


def test1(set1):
    t, c, m = set1
    po = PaddingOracle(t)
    p = po.decrypt4blocks(c)
    assert m == decode(p)

def test2(set2):
    t, c, m = set2
    po = PaddingOracle(t)
    p = po.decrypt4blocks(c)
    assert m == decode(p)
