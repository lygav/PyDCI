from pydci import *
from collections import namedtuple

infinity = float('inf')

Edge = namedtuple('Edge', ('start', 'dest'))


##################################
########## DATA CLASSES ##########
##################################

class Node(object):
    __slots__ = ['name', '_tentative_distance']

    def __init__(self, name):
        self.name = name

    @property
    def tentative_distance(self):
        return self._tentative_distance

    @tentative_distance.setter
    def tentative_distance(self, x):
        self._tentative_distance = x

    def __eq__(self, other):
        return self.name == other.name


class ManhattanGeometry(object):
    def east_neighbor_of(self, a):
        pass

    def south_neighbor_of(self, a):
        pass

    @property
    def root(self):
        return None

    def destination(self):
        pass


##################################
######## pydci INTERACTION #########
##################################

class CalculateShortestPath(Context):
    class Map(Role):

        @property
        def unvisited(self):
            return self.context.unvisited

        @property
        def origin(self):
            return self.root

        @unvisited.setter
        def unvisited(self, unvisited):
            self.context.unvisited = unvisited

        def distance_between(self, a, b):
            return self.distances[Edge(a, b)]

        def nearest_unvisited_node_to_target(self):
            minimum = infinity
            selection = None
            for intersection, unvisited in self.unvisited.items():
                if unvisited:
                    if intersection.tentative_distance < minimum:
                        minimum = intersection.tentative_distance
                        selection = intersection
            return selection

    class CurrentIntersection(Role):

        @property
        def unvisited_neighbors(self):
            ret = []
            if self.context.Map.unvisited.get(self.context.SouthNeighbor):
                ret.append(self.context.SouthNeighbor)
            if self.context.Map.unvisited.get(self.context.EastNeighbor):
                ret.append(self.context.EastNeighbor)
            return ret

    class EastNeighbor(Role):

        def relable_node_as(self, x):
            if x < self.tentative_distance:
                self.tentative_distance = x
                return "distance_was_updated"
            else:
                return "distance_was_not_updated"

    class SouthNeighbor(Role):

        def relable_node_as(self, x):
            if x < self.tentative_distance:
                self.tentative_distance = x
                return "distance_was_updated"
            else:
                return "distance_was_not_updated"

    def __init__(self, origin_node, target_node, geometries, path_vector=None, unvisited_dict=None, pathto_dict=None):
        self.destination = target_node
        self.unvisited = unvisited_dict

        self.rebind(origin_node, geometries)
        self.execute(path_vector, unvisited_dict, pathto_dict)

    def rebind(self, origin_node, geometries):
        self.CurrentIntersection = origin_node
        self.Map = geometries

        map(lambda n: n, geometries.nodes)

        en = self.Map.east_neighbor_of(origin_node)
        if en:
            self.EastNeighbor = en

        sn = self.Map.south_neighbor_of(origin_node)
        if sn:
            self.SouthNeighbor = sn

    def execute(self, path_vector, unvisited_dict, pathto_dict):
        self.do_inits(path_vector, unvisited_dict, pathto_dict)

        unvisited_neighbours = self.CurrentIntersection.unvisited_neighbors
        for neighbor in unvisited_neighbours:
            curr_dist = self.CurrentIntersection.tentative_distance
            dist_btw = self.Map.distance_between(self.CurrentIntersection, neighbor)
            net_distance = curr_dist + dist_btw
            if neighbor.relable_node_as(net_distance) == 'distance_was_updated':
                self.pathTo[neighbor] = self.CurrentIntersection

        self.unvisited.pop(self.CurrentIntersection)

        if len(self.Map.unvisited) == 0:
            self.save_path(self.path)
        else:
            selection = self.Map.nearest_unvisited_node_to_target()
            CalculateShortestPath(selection, self.destination, self.Map, self.path, self.unvisited, self.pathTo)

    def do_inits(self, path_vector, unvisited_dict, pathto_dict):
        if path_vector is None:
            self.unvisited = dict()
            for n in self.Map.nodes:
                self.unvisited[n] = True
                n.tentative_distance = infinity
            self.Map.origin.tentative_distance = 0

            self.path = []
            self.pathTo = dict()

        else:
            self.unvisited = unvisited_dict
            self.path = path_vector
            self.pathTo = pathto_dict

    def save_path(self, path_vector):
        node = self.destination
        while node != None:
            path_vector.append(node)
            node = self.pathTo.get(node)

    def each(self):
        for node in self.path:
            yield node


##################################
############## TEST ##############
##################################

class Geometry1(ManhattanGeometry):
    def __init__(self):
        self.distances = dict()

        names = ["a", "b", "c", "d", "a", "b", "g", "h", "i"]
        self.nodes = [Node(name) for name in names]

        self.a = self.nodes[0]
        self.b = self.nodes[1]
        self.c = self.nodes[2]
        self.d = self.nodes[3]
        self.e = self.nodes[4]
        self.f = self.nodes[5]
        self.g = self.nodes[6]
        self.h = self.nodes[7]
        self.i = self.nodes[8]

        for i in range(9):
            for j in range(9):
                self.distances[Edge(self.nodes[i], self.nodes[j])] = infinity

        self.distances[Edge(self.a, self.b)] = 2
        self.distances[Edge(self.b, self.c)] = 3
        self.distances[Edge(self.c, self.f)] = 1
        self.distances[Edge(self.f, self.i)] = 4
        self.distances[Edge(self.b, self.e)] = 2
        self.distances[Edge(self.e, self.f)] = 1
        self.distances[Edge(self.a, self.d)] = 1
        self.distances[Edge(self.d, self.g)] = 2
        self.distances[Edge(self.g, self.h)] = 1
        self.distances[Edge(self.h, self.i)] = 2
        self.distances[Edge(self.d, self.e)] = 1

        self.next_down_the_street_from = dict()
        self.next_down_the_street_from[self.a] = self.b
        self.next_down_the_street_from[self.b] = self.c
        self.next_down_the_street_from[self.d] = self.e
        self.next_down_the_street_from[self.e] = self.f
        self.next_down_the_street_from[self.g] = self.h
        self.next_down_the_street_from[self.h] = self.i

        self.next_along_the_avenue_from = dict()
        self.next_along_the_avenue_from[self.a] = self.d
        self.next_along_the_avenue_from[self.b] = self.e
        self.next_along_the_avenue_from[self.c] = self.f
        self.next_along_the_avenue_from[self.d] = self.g
        self.next_along_the_avenue_from[self.f] = self.i

    def east_neighbor_of(self, a):
        return self.next_down_the_street_from.get(a, None)

    def south_neighbor_of(self, a):
        return self.next_along_the_avenue_from.get(a, None)

    @property
    def root(self):
        return self.a

    @property
    def destination(self):
        return self.i


if __name__ == '__main__':
    geometry = Geometry1()
    path = CalculateShortestPath(geometry.root, geometry.destination, geometry)
    for n in path.each():
        print(n.name)
