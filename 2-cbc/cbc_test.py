from cbc import encrypt_cbc, decrypt_cbc
import pytest

@pytest.fixture
def key():
    return "140b41b22a29beb4061bda66b6747e14"


@pytest.fixture
def ciphertext1():
    iv = "4ca00ff4c898d61e1edbf1800618fb28"
    c1 = "28a226d160dad07883d04e008a7897ee"
    c2 = "2e4b7465d5290d0c0e6c6822236e1daa"
    c3 = "fb94ffe0c5da05d9476be028ad7c1d81"
    return iv + c1 + c2 + c3


@pytest.fixture
def ciphertext2():
    iv = "5b68629feb8606f9a6667670b75b38a5"
    c1 = "b4832d0f26e1ab7da33249de7d4afc48"
    c2 = "e713ac646ace36e872ad5fb8a512428a"
    c3 = "6e21364b0c374df45503473c5242a253"
    return iv + c1 + c2 + c3


@pytest.fixture
def plaintext1():
    return "Basic CBC mode encryption needs padding."


@pytest.fixture
def plaintext2():
    return "Our implementation uses rand. IV"


def test_decrypt_cbc(ciphertext1, plaintext1, ciphertext2, plaintext2, key):
    assert plaintext1 == decrypt_cbc(ciphertext1, key)
    assert plaintext2 == decrypt_cbc(ciphertext2, key)


def test_cbc(plaintext1, plaintext2, key):
    def test(plaintext, key):
        ciphertexta = encrypt_cbc(plaintext, key)
        ciphertextb = encrypt_cbc(plaintext, key)
        return decrypt_cbc(ciphertexta, key) == decrypt_cbc(ciphertextb, key)
    assert test(plaintext1, key)
    assert test(plaintext1, key)
