import pytest
from authentication import StreamSender, StreamReceiver
import filecmp

@pytest.fixture
def fileset1():
    file = './data/video1.mp4'
    hash0 = '5b96aece304a1422224f9a41b228416028f9ba26b0d1058f400200f06a589949'
    return file, hash0

@pytest.fixture
def fileset2():
    file = './data/video2.mp4'
    hash0 = '03c08f4ee0b576fe319338139c045c89c3e8e9409633bea29442e21425006ea8'
    return file, hash0


def test_authentication1(fileset1):

    f, h0 = fileset1
    fcopy = f + "copy.mp4"
    fstream = f + "stream"

    sender = StreamSender(path=f, buffersize=1024)
    sender.write_file(path=fstream)

    receiver = StreamReceiver(path=fstream, buffersize=1024)
    receiver.write_file(path=fcopy)

    assert h0 == sender.compute_first_hash().hex()
    assert sender.verify_hash()

    assert filecmp.cmp(fcopy, f)


def test_authentication2(fileset2):

    f, h0 = fileset2
    fcopy = f + "copy.mp4"
    fstream = f + "stream"

    sender = StreamSender(path=f, buffersize=1024)
    sender.write_file(path=fstream)

    receiver = StreamReceiver(path=fstream, buffersize=1024)
    receiver.write_file(path=fcopy)

    assert h0 == sender.compute_first_hash().hex()
    assert sender.verify_hash()

    assert filecmp.cmp(fcopy, f)

