__author__ = 'leswing'

# Create a BST
# Calculate num-nodes underneath each sub-tree
# recursive solution

class Tree:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.num_nodes = 1

    def insert(self, value):
        if value < self.value:
            if self.left is None:
                self.left = Tree(value)
                return
            self.left.insert(value)
            return
        if self.right is None:
            self.right = Tree(value)
            return
        self.right.insert(value)

    def count_nodes(self):
        total = 1
        if self.left is not None:
            self.left.count_nodes()
            total += self.left.num_nodes
        if self.right is not None:
            self.right.count_nodes()
            total += self.right.num_nodes
        self.num_nodes = total


def n_choose_k(n, k):
    if 0 <= k <= n:
        ntok = 1
        ktok = 1
        for t in xrange(1, min(k, n - k) + 1):
            ntok *= n
            ktok *= t
            n -= 1
        answer = long(ntok // ktok)
        return answer
    else:
        return 0L


def num_elements_in(tree):
    if tree is None:
        return 0
    return tree.num_nodes


def count_orderings(tree):
    if tree is None:
        return 1
    m = num_elements_in(tree.left)
    n = num_elements_in(tree.right)
    return n_choose_k(m + n, n) * count_orderings(tree.left) * count_orderings(tree.right)


def answer(seq):
    # Create Tree
    root = Tree(seq[0])
    for value in seq[1:]:
        root.insert(value)

    # Count Nodes
    root.count_nodes()

    orderings = count_orderings(root)
    return "%d" % orderings


