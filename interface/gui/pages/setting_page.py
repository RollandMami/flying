import pygame
from ..widget import Button, AnimatedText
from .. import settings
from typing import Callable, Any
from .base_scene import BaseScene
from ..assets import assets


class SettingsScene(BaseScene):

    def __init__(self,
                 master: pygame.Surface,
                 bg: pygame.Color,
                 fg: pygame.Color,
                 on_finished: Callable[..., Any]):
        super().__init__(master, bg, fg, on_finished)
        self.btn_bg = settings.COLOR_BTN_DEFAULT
        self.font = assets.BOPS_FONT(15)
        self.font_title = assets.DIRT_FONT(80)
        cx, _ = self.master.get_rect().center
        mx = self.master.get_rect().right
        bw, bh = 45, 40
        self.btn_home = Button("",
                               bw,
                               bh,
                               self.font,
                               self.btn_bg,
                               self.fg,
                               self.master,
                               (20, 20),
                               lambda: on_finished("HOME"),
                               icon_gap=0,
                               icon=assets.HOME_ICON(30)
                               )
        self.btn_help = Button("",
                               bw,
                               bh,
                               self.font,
                               self.btn_bg,
                               self.fg,
                               self.master,
                               (mx - bw - 20, 20),
                               lambda: on_finished("HELP"),
                               icon_gap=0,
                               icon=assets.HELP_ICON(30)
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
        self.btn_home.update(dt)
        self.btn_help.update(dt)

    def render(self, target: pygame.Surface) -> None:
        target.fill(self.bg)
        self.titre.draw()
        self.btn_home.draw()
        self.btn_help.draw()
