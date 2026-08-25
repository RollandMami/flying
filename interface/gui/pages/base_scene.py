from abc import ABC, abstractmethod
import pygame
from typing import Callable


class BaseScene(ABC):

    def __init__(self,
                 master: pygame.Surface,
                 bg: pygame.Color,
                 fg: pygame.Color,
                 on_finished: Callable) -> None:
        self.master = master
        self.bg = bg
        self.call = on_finished
        self.fg = fg

    @abstractmethod
    def event_handler(self, event: pygame.event.Event) -> None:
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        pass

    @abstractmethod
    def render(self, target: pygame.Surface) -> None:
        pass
