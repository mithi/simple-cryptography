from hashlib import sha256
from collections import deque

class Node:
    def __init__(self, h, l, r, c):
        self.hash = h
        self.left = l
        self.right = r
        self.count = c


class MerkleTree:
    def __init__(self, data):
        # data is a list of bytes
        self.root = None

        if len(data) == 0:
            return

        children = deque()
        parents = deque()

        # create leaf nodes
        for d in data:
            h = sha256(d).digest()
            node = Node(h, None, None, 1)
            children.append(node)

        if len(children) == 1:
            self.root = children[0]
            return

        # create tree
        while True:
            # create next level above
            while True:
                nl = children.popleft()
                nr = children.popleft()
                h = sha256(nl.hash + nr.hash).digest()
                n = Node(h, nl, nr, nl.count + nr.count)
                parents.append(n)

                if len(children) == 1:
                    parents.append(children.popleft())

                if len(children) == 0:
                    children = parents
                    parents = deque()
                    break

            if len(children) == 1:
                self.root = children.popleft()
                break


    def print(self):
        hashes = self.get_hashes()
        for i, level_hashes in enumerate(hashes):
            print(i, ":")
            for h in level_hashes:
                if h != None:
                    print(" > ", h.hex())
                else:
                    print(" > .")

    def get_hashes(self):
        children = deque()
        parents = deque()
        parents.append(self.root)
        hashes = []
        level_hashes = []

        while True:
            node = parents.popleft()
            if node != None:
                level_hashes.append(node.hash)
                children.append(node.left)
                children.append(node.right)
            else:
                level_hashes.append(None)

            if len(parents) == 0:
                parents = children
                hashes.append(level_hashes)
                children = deque()
                level_hashes = []

                if len(parents) == 0:
                    break

        return hashes


def get_test_data():
    data = [b'a', b'b', b'c', b'd', b'e', b'f', b'g']
    hashes = []
    for d in data:
        hashes.append(sha256(d).digest())
    return data, hashes


def test1():
    data, hashes = get_test_data()
    m = MerkleTree([data[0]])
    merkle_hashes = m.get_hashes()
    assert merkle_hashes[0][0] == hashes[0]
    assert merkle_hashes[1][0] == None
    assert merkle_hashes[1][1] == None


def test2():
    data, hashes = get_test_data()
    m = MerkleTree(data[0:2])
    merkle_hashes = m.get_hashes()
    # m.print()
    assert merkle_hashes[0][0] == sha256(hashes[0] + hashes[1]).digest()
    assert merkle_hashes[1][0] == hashes[0]
    assert merkle_hashes[1][1] == hashes[1]
    assert merkle_hashes[2][0] == None
    assert merkle_hashes[2][1] == None
    assert merkle_hashes[2][2] == None
    assert merkle_hashes[2][3] == None


def test3():
    data, hashes = get_test_data()
    m = MerkleTree(data[0:3])
    merkle_hashes = m.get_hashes()
    hash_ab = sha256(hashes[0] + hashes[1]).digest()
    hash_abc = sha256(hash_ab + hashes[2]).digest()
    assert merkle_hashes[0][0] == hash_abc
    assert merkle_hashes[1][0] == hash_ab
    assert merkle_hashes[1][1] == hashes[2]
    assert merkle_hashes[2][0] == hashes[0]
    assert merkle_hashes[2][1] == hashes[1]
    assert merkle_hashes[2][2] == None
    assert merkle_hashes[2][3] == None


def test4():
    data, hashes = get_test_data()
    m = MerkleTree(data[0:4])
    merkle_hashes = m.get_hashes()
    hash_ab = sha256(hashes[0] + hashes[1]).digest()
    hash_cd = sha256(hashes[2] + hashes[3]).digest()
    hash_abcd = sha256(hash_ab + hash_cd).digest()

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
    data, hashes = get_test_data()
    m = MerkleTree(data[0:5])
    merkle_hashes = m.get_hashes()

    hash_ab = sha256(hashes[0] + hashes[1]).digest()
    hash_cd = sha256(hashes[2] + hashes[3]).digest()
    hash_abcd = sha256(hash_ab + hash_cd).digest()
    hash_abcde = sha256(hash_abcd + hashes[4]).digest()

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
    data, hashes = get_test_data()
    m = MerkleTree(data[0:6])
    merkle_hashes = m.get_hashes()

    hash_ab = sha256(hashes[0] + hashes[1]).digest()
    hash_cd = sha256(hashes[2] + hashes[3]).digest()
    hash_ef = sha256(hashes[4] + hashes[5]).digest()

    hash_abcd = sha256(hash_ab + hash_cd).digest()
    hash_abcdef = sha256(hash_abcd + hash_ef).digest()

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
    data, hashes = get_test_data()
    m = MerkleTree(data)
    merkle_hashes = m.get_hashes()

    hash_ab = sha256(hashes[0] + hashes[1]).digest()
    hash_cd = sha256(hashes[2] + hashes[3]).digest()
    hash_ef = sha256(hashes[4] + hashes[5]).digest()

    hash_abcd = sha256(hash_ab + hash_cd).digest()
    hash_efg = sha256(hash_ef + hashes[6]).digest()
    hash_abcdefg = sha256(hash_abcd + hash_efg).digest()


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
