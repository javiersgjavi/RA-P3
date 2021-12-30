from objects.Grid import Grid
from objects.Graph import Graph, Node
from objects.Utils import DDA, get_distance
import pygame
import sys
import numpy as np


class Simulation:
    def __init__(self, path, colors, pixel_size, num_nodes, fps, size_node, distance):
        self.pixel_size = pixel_size
        self.size_node = size_node
        self.grid = Grid(path=path)
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

    def draw(self):
        self.screen.fill(self.colors['white'])

        # draw blocks and nodes
        for x in range(self.gui_shape[0]):
            for y in range(self.gui_shape[1]):
                position = (x, y)
                value = self.grid.get_cell(y, x)

                if (y, x) in self.graph.get_position_nodes():
                    color = self.colors['blue']
                    radio = self.size_node
                    pygame.draw.circle(self.screen, color, (x * self.pixel_size, y * self.pixel_size), radio)

                elif value == 1:
                    color = self.colors['black']
                    rect = pygame.Rect(position[0] * self.pixel_size, position[1] * self.pixel_size, self.pixel_size,
                                       self.pixel_size)
                    pygame.draw.rect(self.screen, color, rect, self.pixel_size)

        # draw edges
        for node_1, node_2 in self.graph.get_edges():

            node_1_pos = node_1.get_position()[1] * self.pixel_size, node_1.get_position()[0] * self.pixel_size
            node_2_pos = node_2.get_position()[1] * self.pixel_size, node_2.get_position()[0] * self.pixel_size

            pygame.draw.line(self.screen, self.colors['red'], node_1_pos, node_2_pos, self.pixel_size)

    def update_gui(self):
        self.draw()
        pygame.display.update()
        self.clock.tick(self.fps)

    def run(self):
        pygame.init()

        self.update_gui()

        while True:

            print('Iteration: ', self.iteration, '-----' * 10)
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
                    # print(p, 1/density)
                    if cell == 0 and ((i, j) not in self.graph.get_position_nodes()) and p < 1 / density:
                        node = Node(position=(i, j))
                        self.graph.add_node(node)
                        node_found = True

            elif not self.graph.is_connected():
                index = self.iteration % self.graph.count_nodes()
                nodes = self.graph.get_nodes()
                current_node = nodes[index]

                position_by_distance = {get_distance(n.get_position(), current_node.get_position()): i for i, n in
                                        enumerate(nodes)}

                for distance in np.sort(list(position_by_distance.keys())):
                    if distance != 0:
                        next_node = nodes[position_by_distance[distance]]
                        dda = DDA(current_node.get_position(), next_node.get_position())
                        path = dda.get_path()
                        if self.grid.check_path_exists(path) and not self.graph.exists_edge(current_node, next_node):  # and next_node not in self.graph.check_neighbours(current_node):
                            self.graph.add_edge(current_node, next_node, distance)
                            break

                print('Generated edges: ', self.graph.count_edges())

            else:

                pass

            self.update_gui()

            self.iteration += 1
