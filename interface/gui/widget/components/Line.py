import pygame


class Line:

    def __init__(self,
                 start: tuple[float, float],
                 end: tuple[float, float],
                 color: pygame.Color | str,
                 width: int = 1) -> None:
        self.start = pygame.Vector2(start)
        self.end = pygame.Vector2(end)
        self.color = color
        self.width = width

    def draw(self, target: pygame.Surface):
        pygame.draw.line(
            target, self.color, self.start, self.end, self.width
        )
