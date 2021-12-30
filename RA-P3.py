from objects.Simulation import Simulation


def main():
    path = './boards/maze_2.png'
    pixel_size = 1
    num_nodes = 50
    fps = 5
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
        colors=colors,
        num_nodes=num_nodes,
        fps=fps
    )

    simulation.run()


if __name__ == '__main__':
    main()
