import itertools


class Graph:
    def __init__(self):
        self.nodes = []
        self.position_nodes = []
        self.edges = []

    def get_nodes(self):
        return self.nodes

    def get_node_by_position(self, position):
        return self.nodes[position]

    def count_nodes(self):
        return len(self.nodes)

    def get_position_nodes(self):
        return self.position_nodes

    def get_edges(self):
        return self.edges

    def count_edges(self):
        return len(self.edges)

    def add_node(self, node):
        self.nodes.append(node)
        self.position_nodes.append(node.get_position())

    def add_edge(self, edge):
        self.edges.append(edge)

class Node:
    new_id = itertools.count()

    def __init__(self, position):
        self.id = next(self.new_id)
        self.position = position
        self.edges = []

    def get_position(self):
        return self.position

    def get_edges(self):
        return self.edges

    def add_edge(self, edge):
        self.edges.append(edge)


class Edge:
    new_id = itertools.count()

    def __init__(self):
        self.id = next(Edge.new_id)
        self.nodes = set()

    def get_id(self):
        return self.id

    def get_nodes(self):
        return self.nodes

    def add_nodes(self, node_1, node_2):
        self.nodes.add(node_1)
        self.nodes.add(node_2)
