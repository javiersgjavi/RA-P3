from objects.Simulation import Simulation


def main():
    path = 'boards/maze_1.png'
    gui = True
    pixel_size = 3
    size_node = pixel_size
    start_point = (5, 10)
    end_point = (80, 155)
    num_nodes = 230
    distance = None
    fps = 60
    colors = {
        'white': (255, 255, 255),
        'black': (0, 0, 0),
        'red': (255, 0, 0),
        'green': (0, 150, 0),
        'blue': (0, 0, 255),
    }

    simulation = Simulation(
        path=path,
        pixel_size=pixel_size,
        size_node=size_node,
        colors=colors,
        num_nodes=num_nodes,
        distance=distance,
        fps=fps,
        start_point=start_point,
        end_point=end_point,
        gui=gui
    )

    simulation.run()


if __name__ == '__main__':
    main()
