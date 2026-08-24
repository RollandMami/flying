from abc import ABC, abstractmethod
import pygame
from typing import Callable


class BaseWidget(ABC):

    def __init__(self,
                text: str,
                width: int,
                height: int,
                font: pygame.font.Font,
                bg_color: str,
                font_color: str,
                master: pygame.Surface,
                position: tuple[int, int],
                call: Callable[..., Any],
                elevation: int = 6) -> None:
        ...

    @abstractmethod
    def draw(self) -> None:
        ...

    @abstractmethod
    def update(self) -> None:
        ...

    @abstractmethod
    def event_handler(self) -> None:
        ...
