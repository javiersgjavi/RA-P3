import numpy as np


def get_distance(pos_1, pos_2):
    return np.sqrt((pos_1[0] - pos_2[0]) ** 2 + (pos_1[1] - pos_2[1]) ** 2)


class DDA:
    def __init__(self, pos1, pos2):
        self.i = pos1[0]
        self.j = pos1[1]
        self.i_2 = pos2[0]
        self.j_2 = pos2[1]
        self.di = pos2[0] - self.i
        self.dj = pos2[1] - self.j
        self.res = []

    def get_path(self):
        # define steps
        steps = max(abs(self.di), abs(self.dj))

        # calculate increments:
        i_inc = self.di / steps
        j_inc = self.dj / steps

        # calculate path

        for i in range(int(steps)):
            self.i += i_inc
            self.j += j_inc
            self.res.append((int(self.i), int(self.j)))
        return self.res


if __name__ == '__main__':
    dda = DDA((0, 0), (7, 11))
    print(dda.get_path())

    dda = DDA((10, 0), (5, 7))
    print(dda.get_path())

    dda = DDA((72, 106), (55, 78))
    print(dda.get_path())
