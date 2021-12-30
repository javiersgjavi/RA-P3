from objects.Grid import Grid
from objects.Graph import Graph, Node
import pygame
import sys
import numpy as np


class Simulation:
    def __init__(self, path, colors, pixel_size, num_nodes, fps):
        self.pixel_size = pixel_size
        self.grid = Grid(path=path)
        self.shape = self.grid.get_shape()
        self.screen = pygame.display.set_mode((self.shape[0] * pixel_size, self.shape[1] * pixel_size))
        self.clock = pygame.time.Clock()
        self.colors = colors
        self.screen.fill(self.colors['white'])
        self.fps = fps
        self.graph = Graph()
        self.num_nodes = num_nodes
        self.edges_generated = False
        self.iteration = 0

    def draw(self):
        self.screen.fill(self.colors['white'])
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                position = (x, y)
                value = self.grid.get_cell(y, x)

                if position in self.graph.get_position_nodes():
                    color = self.colors['blue']
                    radio = self.pixel_size * 5
                    pygame.draw.circle(self.screen, color, position, radio)

                elif value == 1:
                    color = self.colors['black']
                    rect = pygame.Rect(position[0] * self.pixel_size, position[1] * self.pixel_size, self.pixel_size,
                                       self.pixel_size)
                    pygame.draw.rect(self.screen, color, rect, self.pixel_size)

    def update_gui(self):
        self.draw()
        pygame.display.update()
        self.clock.tick(self.fps)

    def run(self):
        pygame.init()

        self.update_gui()
        # pygame.event.grab(True)

        while True:

            print('Iteration: ', self.iteration, '-----' * 10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if self.graph.count_nodes() < self.num_nodes:

                node_found = False
                while not node_found:

                    i = np.random.randint(self.shape[0])
                    j = np.random.randint(self.shape[1])
                    cell = self.grid.get_cell(i, j)
                    if cell == 0 and ((i, j) not in self.graph.get_position_nodes()):
                        node = Node(position=(i, j))
                        self.graph.add_node(node)
                        node_found = True

            elif not self.edges_generated:
                # node = self.graph.get_by_position[self.graph.count_edges()]
                # if ()
                pass

            self.update_gui()

            self.iteration += 1
