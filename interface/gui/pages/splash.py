import pygame
from ..widget import ProgressBar, AnimatedText
from .. import settings
from .base_scene import BaseScene
from typing import Callable
from ..assets import assets


class SplashScene(BaseScene):

    def __init__(self,
                 master: pygame.Surface,
                 bg: pygame.Color,
                 fg: pygame.Color,
                 on_finished: Callable) -> None:
        super().__init__(master, bg, fg, on_finished)
        self.width, self.height = master.get_width(), master.get_height()
        self.font = assets.BOPS_FONT(20)
        self.font_title = assets.DIRT_FONT(80)
        self.prog = ProgressBar(settings.COLOR_BTN_DEFAULT,
                                self.font,
                                settings.COLOR_TEXT_PRIMARY,
                                self.master, (10, self.height - 35),
                                duration=4)
        self.text = AnimatedText(
            self.master,
            self.font_title,
            "F L Y - I N G",
            self.fg,
            delay=0.08
        )
        self._isfinished = False

    def event_handler(self, evt: pygame.event.Event) -> None:
        pass

    def render(self, target: pygame.Surface) -> None:
        target.fill(self.bg)
        self.prog.draw()
        self.text.draw()

    def update(self, dt: float) -> None:
        self.prog.update(dt)
        self.text.update(dt)
        if self.prog.is_finished and self.text.is_finished \
           and not self._isfinished:
            self._isfinished = True
            self.call("HOME")
