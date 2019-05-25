from merkletree import MerkleTree
from hashlib import sha256

data = [b'a', b'b', b'c', b'd', b'e', b'f', b'g']
hashes = []

for d in data:
    hashes.append(sha256(d).digest())

hash_ab = sha256(hashes[0] + hashes[1]).digest()
hash_cd = sha256(hashes[2] + hashes[3]).digest()
hash_ef = sha256(hashes[4] + hashes[5]).digest()
hash_abc = sha256(hash_ab + hashes[2]).digest()
hash_efg = sha256(hash_ef + hashes[6]).digest()

hash_abcd = sha256(hash_ab + hash_cd).digest()
hash_abcde = sha256(hash_abcd + hashes[4]).digest()
hash_abcdef = sha256(hash_abcd + hash_ef).digest()
hash_abcdefg = sha256(hash_abcd + hash_efg).digest()

def test1():
    m = MerkleTree([data[0]])
    merkle_hashes = m.get_hashes()
    assert merkle_hashes[0][0] == hashes[0]
    assert merkle_hashes[1][0] == None
    assert merkle_hashes[1][1] == None


def test2():
    m = MerkleTree(data[0:2])
    merkle_hashes = m.get_hashes()

    assert merkle_hashes[0][0] == sha256(hashes[0] + hashes[1]).digest()
    assert merkle_hashes[1][0] == hashes[0]
    assert merkle_hashes[1][1] == hashes[1]
    for h in merkle_hashes[2]:
        assert h == None

def test3():
    m = MerkleTree(data[0:3])
    merkle_hashes = m.get_hashes()

    assert merkle_hashes[0][0] == hash_abc
    assert merkle_hashes[1][0] == hash_ab
    assert merkle_hashes[1][1] == hashes[2]
    assert merkle_hashes[2][0] == hashes[0]
    assert merkle_hashes[2][1] == hashes[1]
    assert merkle_hashes[2][2] == None
    assert merkle_hashes[2][3] == None


def test4():
    m = MerkleTree(data[0:4])
    merkle_hashes = m.get_hashes()

    assert merkle_hashes[0][0] == hash_abcd
    assert merkle_hashes[1][0] == hash_ab
    assert merkle_hashes[1][1] == hash_cd
    assert merkle_hashes[2][0] == hashes[0]
    assert merkle_hashes[2][1] == hashes[1]
    assert merkle_hashes[2][2] == hashes[2]
    assert merkle_hashes[2][3] == hashes[3]

    for n in merkle_hashes[3]:
        assert n == None


def test5():
    m = MerkleTree(data[0:5])
    merkle_hashes = m.get_hashes()

    assert merkle_hashes[0][0] == hash_abcde
    assert merkle_hashes[1][0] == hash_abcd
    assert merkle_hashes[1][1] == hashes[4]
    assert merkle_hashes[2][0] == hash_ab
    assert merkle_hashes[2][1] == hash_cd
    assert merkle_hashes[2][2] == None
    assert merkle_hashes[2][3] == None

    assert merkle_hashes[3][0] == hashes[0]
    assert merkle_hashes[3][1] == hashes[1]
    assert merkle_hashes[3][2] == hashes[2]
    assert merkle_hashes[3][3] == hashes[3]


def test6():
    m = MerkleTree(data[0:6])
    merkle_hashes = m.get_hashes()

    assert merkle_hashes[0][0] == hash_abcdef
    assert merkle_hashes[1][0] == hash_abcd
    assert merkle_hashes[1][1] == hash_ef
    assert merkle_hashes[2][0] == hash_ab
    assert merkle_hashes[2][1] == hash_cd
    assert merkle_hashes[2][2] == hashes[4]
    assert merkle_hashes[2][3] == hashes[5]

    assert merkle_hashes[3][0] == hashes[0]
    assert merkle_hashes[3][1] == hashes[1]
    assert merkle_hashes[3][2] == hashes[2]
    assert merkle_hashes[3][3] == hashes[3]
    assert merkle_hashes[3][4] == None
    assert merkle_hashes[3][5] == None
    assert merkle_hashes[3][6] == None
    assert merkle_hashes[3][7] == None


def test7():
    m = MerkleTree(data)
    merkle_hashes = m.get_hashes()

    assert merkle_hashes[0][0] == hash_abcdefg
    assert merkle_hashes[1][0] == hash_abcd
    assert merkle_hashes[1][1] == hash_efg
    assert merkle_hashes[2][0] == hash_ab
    assert merkle_hashes[2][1] == hash_cd
    assert merkle_hashes[2][2] == hash_ef
    assert merkle_hashes[2][3] == hashes[6]

    assert merkle_hashes[3][0] == hashes[0]
    assert merkle_hashes[3][1] == hashes[1]
    assert merkle_hashes[3][2] == hashes[2]
    assert merkle_hashes[3][3] == hashes[3]
    assert merkle_hashes[3][4] == hashes[4]
    assert merkle_hashes[3][5] == hashes[5]
    assert merkle_hashes[3][6] == None
    assert merkle_hashes[3][7] == None

    m.print()

if __name__ == '__main__':
    test1()
    test2()
    test3()
    test4()
    test5()
    test6()
    test7()
