import pygame
from typing import Callable, Any, Optional
from .base_scene import BaseScene
from configparser import ConfigParser
from functools import partial
from ..assets import assets
from ..widget import (
    Button,
    AnimatedText,
    Grid)


class GameScene(BaseScene):

    def __init__(self,
                 master: pygame.Surface,
                 bg: pygame.Color,
                 fg: pygame.Color,
                 on_finished: Callable[..., Any],
                 config: Optional[ConfigParser]) -> None:
        super().__init__(master, bg, fg, on_finished, config)
        self.btn_bg = self.cfg.get("color-theme", "COLOR_BTN_DEFAULT")
        self.bttm_bg = self.cfg.get("color-theme", "COLOR_BTN_ACCENT")
        self.hover_bg = self.cfg.get("color-theme", "COLOR_BTN_HOVER")
        self.font = assets.BOPS_FONT(15)
        self.font_title = assets.DIRT_FONT(80)
        mrect = self.master.get_rect()
        cx, _ = mrect.center
        my = mrect.bottom
        bw, bh = 45, 40
        my = my - bh - 20
        self.base_btn = partial(
            Button, width=bw, height=bh, font=self.font, bg_color=self.btn_bg,
            bottom_color=self.bttm_bg, hover_color=self.hover_bg,
            font_color=self.fg, master=self.master
        )
        self.btn_home = self.base_btn(
                               text="",
                               position=(20, my),
                               call=lambda: on_finished("HOME"),
                               icon_gap=0,
                               icon=assets.HOME_ICON(30)
                               )
        self.btn_setting = self.base_btn(
                               text="",
                               position=(20 + bw + 20, my),
                               call=lambda: on_finished("SETTINGS"),
                               icon_gap=0,
                               icon=assets.SETTING_ICON(30)
                               )
        self.titre = AnimatedText(
                    self.master, self.font_title,
                    "R E A D Y", self.fg, 0, 0
        )
        self.grid = Grid(None, self.bg, self.fg, self.master, (80, 80), 40)

    def event_handler(self, event: pygame.event.Event) -> None:
        pass

    def update(self, dt: float) -> None:
        self.titre.update(dt)
        self.btn_home.update(dt)
        self.btn_setting.update(dt)

    def render(self, target: pygame.Surface) -> None:
        target.fill(self.bg)
        self.grid.draw()
        self.titre.draw()
        self.btn_home.draw()
        self.btn_setting.draw()
