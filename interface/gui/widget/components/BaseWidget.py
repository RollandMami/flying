from abc import ABC, abstractmethod
import pygame


class BaseWidget(ABC):

    def __init__(self,
                 font: pygame.font.Font,
                 bg_color: pygame.Color,
                 font_color: pygame.Color,
                 master: pygame.Surface,
                 ) -> None:
        self.master = master
        self.bg = bg_color
        self.font = font
        self.fg = font_color

    @abstractmethod
    def draw(self) -> None:
        ...

    @abstractmethod
    def update(self, dt: float) -> None:
        ...

    @abstractmethod
    def event_handler(self) -> None:
        ...
