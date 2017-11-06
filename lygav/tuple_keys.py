
from collections import namedtuple

Edge = namedtuple('Edge', ('start', 'dest'))

edges = dict()

class Node(object):
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        # return id(self) == id(other)
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)
        return id(self)


e1 = Edge(Node(1), Node(2))
e2 = Edge(Node(3), Node(4))

edges[e1] = 'e1'
edges[e2] = 'e2'


e11 = Edge(Node(1), Node(2))

print(edges)
print(e1 == e11)
print(edges[e1])
print(edges[e11])
print(e11 in edges.keys())