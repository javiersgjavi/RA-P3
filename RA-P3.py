from objects.Simulation import Simulation


def main():
    path = './boards/maze_1.png'
    pixel_size = 4
    size_node = pixel_size
    num_nodes = 200
    distance = 200
    fps = 60
    colors = {
        'white': (255, 255, 255),
        'black': (0, 0, 0),
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
    }

    simulation = Simulation(
        path=path,
        pixel_size=pixel_size,
        size_node=size_node,
        colors=colors,
        num_nodes=num_nodes,
        distance=distance,
        fps=fps
    )

    simulation.run()


if __name__ == '__main__':
    main()
