import cv2
import numpy as np


class Grid:
    def __init__(self, path):

        image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        grid = np.array(image)
        self.width = grid.shape[0]
        self.height = grid.shape[1]
        self.board = np.where(grid == 0, 1, 0)

    def is_valid(self, x, y):
        res = True
        if x < 0 or x >= self.width:
            res = False
        if y < 0 or y >= self.height:
            res = False
        return res

    def get_board(self):
        return self.board

    def get_cell(self, x, y):
        res = None
        if self.is_valid(x, y):
            return self.board[x, y]
        return res

    def check_path_exists(self, path):
        res = True
        for p in path:
            if self.get_cell(p[0], p[1]) == 1:
                res = False
                break
        return res

    def get_shape(self):
        return self.width, self.height

    def print_board(self):
        print(self.board)

