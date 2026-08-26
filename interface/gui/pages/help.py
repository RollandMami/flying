import pygame
from ..widget import Button, AnimatedText
from .. import settings
from typing import Callable, Any
from .base_scene import BaseScene
from ..assets import assets


class HelpScene(BaseScene):

    def __init__(self,
                 master: pygame.Surface,
                 bg: pygame.Color,
                 fg: pygame.Color,
                 on_finished: Callable[..., Any]):
        super().__init__(master, bg, fg, on_finished)
        self.btn_bg = settings.COLOR_BTN_DEFAULT
        self.font = assets.BOPS_FONT(15)
        self.font_title = assets.DIRT_FONT(80)
        cx, cy = self.master.get_rect().center
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
        self.btn_setting = Button(
                               "",
                               bw,
                               bh,
                               self.font,
                               self.btn_bg,
                               self.fg,
                               self.master,
                               (mx - bw - 20, 20),
                               lambda: on_finished("SETTINGS"),
                               icon_gap=0,
                               icon=assets.SETTING_ICON(30)
                               )
        self.titre = AnimatedText(
                    self.master,
                    self.font_title,
                    "H E L P",
                    self.fg,
                    0, 50 - cy
        )

    def event_handler(self, event: pygame.event.Event) -> None:
        pass

    def update(self, dt: float) -> None:
        self.titre.update(dt)
        self.btn_home.update(dt)
        self.btn_setting.update(dt)

    def render(self, target: pygame.Surface) -> None:
        target.fill(self.bg)
        self.titre.draw()
        self.btn_home.draw()
        self.btn_setting.draw()
