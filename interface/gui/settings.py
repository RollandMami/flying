import webcolors


def rainbow() -> list[tuple[int, int, int]]:
    return [
        webcolors.hls_to_rgb(((index % 7) * (360.0 / 7) / 360.0, 0.5, 1.0))
        for index in range(7)
    ]


#                      DIMENSION DES SPRITES C'EST 120 (H) X 80 (V) SCAN + IDLE
#                           DIMENSION DES SPRITES C'EST 120 (H) X 100 (V) DEATH
#                           DIMENSION DES SPRITES C'EST 120 (H) X 100 (V) DEATH
