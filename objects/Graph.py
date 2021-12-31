import itertools
from objects.Utils import get_distance
import networkx as nx


class Graph:
    def __init__(self):
        self.graph = nx.Graph()
        self.position_nodes = []

    def get_shortest_path(self):
        return nx.shortest_path(self.graph)

    def get_nodes(self):
        return self.graph.nodes()

    def get_node_by_position(self, position):
        res = None
        nodes = self.get_nodes()
        for node in nodes:
            if node.get_position() == position:
                return res

        return res

    def get_position_nodes(self):
        return self.position_nodes

    def get_nodes(self):
        return list(self.graph.nodes())

    def count_nodes(self):
        return self.graph.number_of_nodes()

    def get_edges(self):
        return self.graph.edges()

    def count_edges(self):
        return self.graph.number_of_edges()

    def add_node(self, node):
        self.graph.add_node(node)
        self.position_nodes.append(node.get_position())

    def add_edge(self, node1, node2, weight):
        self.graph.add_edge(node1, node2, weight=weight)

    def exists_edge(self, node1, node2):
        return self.graph.has_edge(node1, node2)

    def get_density(self, position, distance):
        res = 1
        if distance:
            nodes = self.get_nodes()
            for node in nodes:
                if get_distance(position, node.get_position()) <= distance:
                    res += 1
        return res

    def check_neigbours(self, node):
        neighbours = set()
        edges = node.get_edges()
        for edge in edges:
            neighbours.add(self.get_other_node(edge, node))

        initial_neighbours = neighbours.copy()
        for n in initial_neighbours:
            for edge in n.get_edges():
                neighbours.add(self.get_other_node(edge, n))

        return neighbours

    def is_connected(self):
        return nx.is_connected(self.graph)

    def get_weight_edge(self, node_1, node_2):
        return self.graph.get_edge_data(node_1, node_2)['weight']


def get_other_node(edge, node):
    nodes = edge.get_nodes()
    if nodes[0] == node:
        return nodes[1]
    else:
        return nodes[0]


class Node:
    new_id = itertools.count()

    def __init__(self, position):
        self.id = next(self.new_id)
        self.position = position
        self.edges = []

    def get_position(self):
        return self.position
