import pygame
import sys
from ..widget import Button, ProgressBar
from functools import partial
from .. import settings
from .base_scene import BaseScene


class SplashScene(BaseScene):

    def __init__(self,
                 master: pygame.Surface,
                 bg: pygame.Color) -> None:
        self.master = master
        self.bg = bg
        self.font = pygame.font.SysFont("impact", 26)
        self.AppButton = partial(
                            Button,
                            width=80,
                            height=25,
                            font=self.font,
                            bg_color=settings.COLOR_BTN_DEFAULT,
                            font_color=settings.COLOR_TEXT_PRIMARY,
                            master=self.master,
                            elevation=4)
        self.btn_test = self.AppButton(
            text="test",
            position=(200, 200),
            call=lambda: print("hello world"),
        )
        self.prog = ProgressBar(settings.COLOR_BTN_DEFAULT,
                                self.font,
                                settings.COLOR_TEXT_PRIMARY,
                                self.master, (10, 690), duration=5)

    def event_handler(self, evt: pygame.event.Event) -> None:
        pass

    def render(self, target: pygame.Surface) -> None:
        target.fill(self.bg)
        self.btn_test.draw()
        self.prog.draw()

    def update(self, dt: float) -> None:
        self.prog.update(dt)
