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
    def _build_widget(self) -> None:
        ...

    @abstractmethod
    def event_handler(self, event: pygame.event.Event) -> None:
        ...

    @abstractmethod
    def update(self, dt: float) -> None:
        ...

    @abstractmethod
    def render(self, target: pygame.Surface) -> None:
        ...

    def on_resize(self, new_width: int, new_height: int) -> None:
        if hasattr(self, "ui_manager"):
            self.ui_manager.set_window_resolution(
                (new_width, new_height))
            self.ui_manager.clear_and_reset()
        self._build_widget()
