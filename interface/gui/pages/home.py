import pygame
from ..widget import AnimatedText
from .base_scene import BaseScene
from typing import Callable


class HomeScene(BaseScene):
    def __init__(self,
                 master: pygame.Surface,
                 bg: pygame.Color,
                 fg: pygame.Color,
                 on_finished: Callable) -> None:
        super().__init__(master, bg, fg, on_finished)
        self.width, self.height = master.get_width(), master.get_height()
        self.font = pygame.font.SysFont("impact", 26)
        self.font_title = pygame.font.SysFont("dejavusans", 80)
        self.text = AnimatedText(
            self.master,
            self.font_title,
            "h o m e",
            self.fg,
            delay=0.08
        )

    def event_handler(self, evt: pygame.event.Event) -> None:
        pass

    def render(self, target: pygame.Surface) -> None:
        target.fill(self.bg)
        self.text.draw()

    def update(self, dt: float) -> None:
        self.text.update(dt)
