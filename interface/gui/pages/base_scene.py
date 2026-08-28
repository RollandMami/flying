from abc import ABC, abstractmethod
import pygame
from typing import Callable, Any
from configparser import ConfigParser


class BaseScene(ABC):

    def __init__(self,
                 master: pygame.Surface,
                 bg: pygame.Color,
                 fg: pygame.Color,
                 on_finished: Callable[..., Any],
                 config: ConfigParser
                 ) -> None:
        self.master = master
        self.bg = bg
        self.call = on_finished
        self.fg = fg
        self.cfg = config

    @abstractmethod
    def event_handler(self, event: pygame.event.Event) -> None:
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        pass

    @abstractmethod
    def render(self, target: pygame.Surface) -> None:
        pass
