from ctr import encrypt_ctr, decrypt_ctr
import pytest

@pytest.fixture
def key():
    return "36f18357be4dbd77f050515c73fcf9f2"


@pytest.fixture
def ciphertext1():
    iv = "69dda8455c7dd4254bf353b773304eec"
    c1 = "0ec7702330098ce7f7520d1cbbb20fc3"
    c2 = "88d1b0adb5054dbd7370849dbf0b88d3"
    c3 = "93f252e764f1f5f7ad97ef79d59ce29f"
    c4 = "5f51eeca32eabedd9afa9329"
    return iv + c1 + c2 + c3 + c4


@pytest.fixture
def ciphertext2():
    iv = "770b80259ec33beb2561358a9f2dc617"
    c1 = "e46218c0a53cbeca695ae45faa8952aa"
    c2 = "0e311bde9d4e01726d3184c34451"
    return iv + c1 + c2


@pytest.fixture
def plaintext1():
    return "CTR mode lets you build a stream cipher from a block cipher."


@pytest.fixture
def plaintext2():
    return "Always avoid the two time pad!"


def test_decrypt_ctr(ciphertext1, plaintext1, ciphertext2, plaintext2, key):
    assert plaintext1 == decrypt_ctr(ciphertext1, key)
    assert plaintext2 == decrypt_ctr(ciphertext2, key)


def test_ctr(plaintext1, plaintext2, key):
    def test(plaintext, key):
        ciphertexta = encrypt_ctr(plaintext, key)
        ciphertextb = encrypt_ctr(plaintext, key)
        return decrypt_ctr(ciphertexta, key) == decrypt_ctr(ciphertextb, key)
    assert test(plaintext1, key)
    assert test(plaintext1, key)
