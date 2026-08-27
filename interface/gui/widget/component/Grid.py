from .BaseWidget import BaseWidget
import pygame
from .Line import Line


class Grid(BaseWidget):

    def __init__(self,
                 font: pygame.font.Font | None,
                 bg_color: pygame.Color,
                 font_color: pygame.Color,
                 master: pygame.Surface,
                 spicing: tuple[int, int],
                 alpha: int = 80):
        super().__init__(font, bg_color, font_color, master)
        self.mrect = self.master.get_rect()
        self.width = self.mrect.width
        self.height = self.mrect.height
        self.sx, self.sy = spicing

        line_color = pygame.Color(font_color)
        line_color.a = alpha

        self.overlay = pygame.Surface((self.width, self.height),
                                      pygame.SRCALPHA)
        self.columns: list[Line] = [
            Line((x, 0), (x, self.height), line_color)
            for x in range(0, self.width, self.sx)
        ]
        self.rows: list[Line] = [
            Line((0, y), (self.width, y), line_color)
            for y in range(0, self.height, self.sy)
        ]

        for col in self.columns:
            col.draw(self.overlay)
        for row in self.rows:
            row.draw(self.overlay)

    def draw(self) -> None:
        self.master.blit(self.overlay, (0, 0))

    def update(self, dt: float) -> None:
        pass

    def event_handler(self) -> None:
        pass
