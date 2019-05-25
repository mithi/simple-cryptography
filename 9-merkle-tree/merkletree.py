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

        children, parents = deque(), deque()

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
            # create the next level abo e
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

    def get_hashes(self):
        hashes, level_hashes = [], []
        children, parents = deque(), deque()
        parents.append(self.root)

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

    def print(self):
        hashes = self.get_hashes()
        for i, level_hashes in enumerate(hashes):
            print("*", i)
            for h in level_hashes:
                if h != None:
                    print(" > ", h.hex())
                else:
                    print(" > .")
