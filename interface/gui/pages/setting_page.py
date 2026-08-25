import pygame
from ..widget import Button, AnimatedText
from .. import settings
from typing import Callable, Any
from .base_scene import BaseScene


class SettingsScene(BaseScene):

    def __init__(self,
                 master: pygame.Surface,
                 bg: pygame.Color,
                 fg: pygame.Color,
                 on_finished: Callable[..., Any]):
        super().__init__(master, bg, fg, on_finished)
        self.btn_bg = settings.COLOR_BTN_DEFAULT
        self.font = pygame.font.SysFont("dejavusans", 15)
        self.font_title = pygame.font.SysFont("dejavusans", 80)
        cx, cy = self.master.get_rect().center
        bw, bh = 60, 50
        self.btn_start = Button("H",
                                bw,
                                bh,
                                self.font,
                                self.btn_bg,
                                self.fg,
                                self.master,
                                (20, 20),
                                lambda: on_finished("HOME")
                                )
        self.titre = AnimatedText(
                    self.master,
                    self.font_title,
                    "S E T T I N G",
                    self.fg,
                    0, 0
        )

    def event_handler(self, event: pygame.event.Event) -> None:
        pass

    def update(self, dt: float) -> None:
        self.titre.update(dt)
        self.btn_start.update(dt)

    def render(self, target: pygame.Surface) -> None:
        target.fill(self.bg)
        self.titre.draw()
        self.btn_start.draw()
