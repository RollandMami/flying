# from infrastructure import MapModel, TxtParser
from interface import Window, settings
import pygame


def main() -> None:
    # path = "maps/challenger/01_the_impossible_dream.txt"
    bg = pygame.Color(settings.COLOR_BG_MAIN)
    width = settings.WIDTH
    height = settings.HEIGHT
    win = Window(bg, "Test sur le main", width, height)
    win.run()
    print("\n\nHello from flyin!")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
