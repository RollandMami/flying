import webcolors

WIDTH = 1280
HEIGHT = 720
MAPDIR = "../maps"

# color theme:



def rainbow() -> list[tuple[int, int, int]]:
    return [
        webcolors.hsl_to_rgb(((index % 7) * (360.0 / 7) / 360.0, 0.5, 1.0))
        for index in range(7)
    ]