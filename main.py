# from infrastructure import MapModel, TxtParser
from interface import SceneManager
# import pygame
from configparser import ConfigParser


def main() -> None:
    config = ConfigParser()
    with open("config.ini", "r") as file:
        config.read_file(file)
    width = config.getint("display", "width")
    height = config.getint("display", "height")
    win = SceneManager(width, height, "F L Y - I N G")
    win.run()
    print("\n\nHello from flyin!")


if __name__ == "__main__":
    # try:
    #    main()
    # except Exception as e:
    #    print(e)
    main()
