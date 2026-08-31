import pygame
from ..widget import ProgressBar, AnimatedText
from .base_scene import BaseScene
from typing import Callable, Any
from configparser import ConfigParser
from ..assets import assets


class SplashScene(BaseScene):

    def __init__(self,
                 master: pygame.Surface,
                 bg: pygame.Color,
                 fg: pygame.Color,
                 on_finished: Callable[..., Any],
                 config: ConfigParser) -> None:
        super().__init__(master, bg, fg, on_finished, config)
        self.font = assets.BOPS_FONT(20)
        self.font_title = assets.DIRT_FONT(80)
        self.prog_bg = pygame.Color(
            self.cfg.get("color-theme", "COLOR_BTN_DEFAULT"))
        self.prog_fg = pygame.Color(
            self.cfg.get("color-theme", "COLOR_TEXT_PRIMARY"))
        self._isfinished = False
        self._build_widget()

    def _build_widget(self) -> None:
        self.width = self.master.get_width()
        self.height = self.master.get_height()
        self.prog = ProgressBar(
            self.prog_bg, self.font, self.prog_fg,
            self.master, (10, self.height - 35),
            duration=4)
        self.text = AnimatedText(
            self.master,
            self.font_title,
            "F L Y - I N G",
            self.fg,
            delay=0.08
        )

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
