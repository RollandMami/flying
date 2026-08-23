# from infrastructure import MapModel, TxtParser
from interface import SceneManager, settings
import pygame


def main() -> None:
    # path = "maps/challenger/01_the_impossible_dream.txt"
    width = settings.WIDTH
    height = settings.HEIGHT
    win = SceneManager(width, height, "Test sur le main")
    win.run()
    print("\n\nHello from flyin!")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
