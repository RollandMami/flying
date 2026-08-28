# from infrastructure import MapModel, TxtParser
from interface import SceneManager
# import pygame
from configparser import ConfigParser


def main() -> None:
    config = ConfigParser()
    with open("config.ini", "r") as file:
        config.read_file(file)
    win = SceneManager("F L Y - I N G", config)
    win.run()


if __name__ == "__main__":
    # try:
    #    main()
    # except Exception as e:
    #    print(e)
    main()
