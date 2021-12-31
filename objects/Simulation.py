from objects.Grid import Grid
from objects.Graph import Graph, Node
from objects.Utils import DDA, get_distance
import pygame
import sys
import numpy as np
import os


class Simulation:
    def __init__(self, path, colors, pixel_size, num_nodes, fps, size_node, distance, start_point, end_point):
        self.path_image = path
        self.pixel_size = pixel_size
        self.size_node = size_node
        self.grid = Grid(path=self.path_image)
        self.grid_shape = self.grid.get_shape()
        self.gui_shape = (self.grid_shape[1], self.grid_shape[0])
        self.screen = pygame.display.set_mode((self.gui_shape[0] * pixel_size, self.gui_shape[1] * pixel_size))
        self.clock = pygame.time.Clock()
        self.colors = colors
        self.screen.fill(self.colors['white'])
        self.fps = fps
        self.graph = Graph()
        self.num_nodes = num_nodes
        self.edges_generated = False
        self.iteration = 0
        self.distance = distance
        self.start_point = start_point
        self.end_point = end_point

    def draw_edge(self, position_1, position_2):
        node_1_pos = position_1[1] * self.pixel_size, position_1[0] * self.pixel_size
        node_2_pos = position_2[1] * self.pixel_size, position_2[0] * self.pixel_size

        pygame.draw.line(self.screen, self.colors['red'], node_1_pos, node_2_pos, self.pixel_size)

    def draw(self):
        self.screen.fill(self.colors['white'])

        # draw edges
        for node_1, node_2 in self.graph.get_edges():
            self.draw_edge(node_1.get_position(), node_2.get_position())

        # draw blocks and nodes
        for x in range(self.gui_shape[0]):
            for y in range(self.gui_shape[1]):
                position = (x, y)
                value = self.grid.get_cell(y, x)

                if (y, x) == self.start_point or (y, x) == self.end_point:
                    color = self.colors['green']
                    radio = self.size_node
                    pygame.draw.circle(self.screen, color, (x * self.pixel_size, y * self.pixel_size), radio * 2)

                elif (y, x) in self.graph.get_position_nodes():
                    color = self.colors['blue']
                    radio = self.size_node
                    pygame.draw.circle(self.screen, color, (x * self.pixel_size, y * self.pixel_size), radio)

                elif value == 1:
                    color = self.colors['black']
                    rect = pygame.Rect(position[0] * self.pixel_size, position[1] * self.pixel_size, self.pixel_size,
                                       self.pixel_size)
                    pygame.draw.rect(self.screen, color, rect, self.pixel_size)

    def draw_path(self, path):
        positions = [node.get_position() for node in path]

        self.screen.fill(self.colors['white'])

        # draw selected edges
        for i in range(1, len(path)):
            node_1 = path[i - 1]
            node_2 = path[i]
            self.draw_edge(node_1.get_position(), node_2.get_position())

        # draw blocks and nodes
        for x in range(self.gui_shape[0]):
            for y in range(self.gui_shape[1]):
                position = (x, y)
                value = self.grid.get_cell(y, x)

                # draw special points
                if (y, x) == self.start_point or (y, x) == self.end_point:
                    color = self.colors['green']
                    radio = self.size_node
                    pygame.draw.circle(self.screen, color, (x * self.pixel_size, y * self.pixel_size), radio * 2)

                # draw selected nodes
                elif (y, x) in positions:
                    color = self.colors['blue']
                    radio = self.size_node
                    pygame.draw.circle(self.screen, color, (x * self.pixel_size, y * self.pixel_size), radio)

                # draw walls
                elif value == 1:
                    color = self.colors['black']
                    rect = pygame.Rect(position[0] * self.pixel_size, position[1] * self.pixel_size, self.pixel_size,
                                       self.pixel_size)
                    pygame.draw.rect(self.screen, color, rect, self.pixel_size)

    def update_gui(self, path=None):
        if path:
            self.draw_path(path)
        else:
            self.draw()
        pygame.display.update()
        self.clock.tick(self.fps)
        if path:
            if not os.path.exists('./results/'):
                os.makedirs('./results/')
            name = self.path_image.split('/')[-1]
            pygame.image.save(self.screen, f'./results/{name}')

    def add_edge(self, current_node, nodes):
        position_by_distance = {get_distance(n.get_position(), current_node.get_position()): i for i, n in
                                enumerate(nodes)}

        for distance in np.sort(list(position_by_distance.keys())):
            if distance != 0:
                next_node = nodes[position_by_distance[distance]]
                dda = DDA(current_node.get_position(), next_node.get_position())
                path = dda.get_path()
                if self.grid.check_path_exists(path) and not self.graph.exists_edge(current_node, next_node):
                    self.graph.add_edge(current_node, next_node, distance)
                    break

    def get_or_create_node(self, position):
        if position not in self.graph.get_position_nodes():
            node = Node(position=position)
            self.graph.add_node(node)
            nodes = self.graph.get_nodes()
            self.add_edge(node, nodes)

        else:
            node = self.graph.get_node_by_position(position)

        return node

    def generate_graph(self):
        loop = True

        while loop:

            #print('Iteration: ', self.iteration, '-----' * 10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if self.graph.count_nodes() < self.num_nodes:

                node_found = False
                while not node_found:

                    i = np.random.randint(self.grid_shape[0])
                    j = np.random.randint(self.grid_shape[1])

                    cell = self.grid.get_cell(i, j)
                    p = np.random.uniform(0, 1)
                    density = self.graph.get_density((i, j), self.distance)

                    if cell == 0 and ((i, j) not in self.graph.get_position_nodes()) and p < 1 / density:
                        node = Node(position=(i, j))
                        self.graph.add_node(node)
                        node_found = True

            elif not self.graph.is_connected():
                index = self.iteration % self.graph.count_nodes()
                nodes = self.graph.get_nodes()
                current_node = nodes[index]
                self.add_edge(current_node, nodes)

            else:
                start_node = self.get_or_create_node(self.start_point)
                end_node = self.get_or_create_node(self.end_point)
                loop = False

            self.update_gui()
            self.iteration += 1

        return start_node, end_node

    def find_sortest_path(self, start_node, end_node):
        path = self.graph.get_shortest_path()[start_node][end_node]
        return path

    def run(self):
        pygame.init()
        self.update_gui()

        start_node, end_node = self.generate_graph()
        print(f'Generated graph with {self.graph.count_nodes()} nodes and {self.graph.count_edges()} edges')
        path = self.find_sortest_path(start_node, end_node)

        self.update_gui(path)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


