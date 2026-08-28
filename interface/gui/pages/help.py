import pygame
from ..widget import Button, AnimatedText
from typing import Callable, Any
from .base_scene import BaseScene
from ..assets import assets
from configparser import ConfigParser
from functools import partial


class HelpScene(BaseScene):

    def __init__(self,
                 master: pygame.Surface,
                 bg: pygame.Color,
                 fg: pygame.Color,
                 on_finished: Callable[..., Any],
                 config: ConfigParser) -> None:
        super().__init__(master, bg, fg, on_finished, config)
        btn_bg = self.cfg.get("color-theme", "COLOR_BTN_DEFAULT")
        bttm_bg = self.cfg.get("color-theme", "COLOR_BTN_ACCENT")
        hover_bg = self.cfg.get("color-theme", "COLOR_BTN_HOVER")

        self.btn_bg = pygame.Color(btn_bg)
        self.bttm_bg = pygame.Color(bttm_bg)
        self.hover_bg = pygame.Color(hover_bg)
        self.font = assets.BOPS_FONT(15)
        self.font_title = assets.DIRT_FONT(80)
        cx, cy = self.master.get_rect().center
        mx = self.master.get_rect().right
        bw, bh = 45, 40
        self.base_btn = partial(
            Button, width=bw, height=bh, font=self.font, bg_color=self.btn_bg,
            bottom_color=self.bttm_bg, hover_color=self.hover_bg,
            font_color=self.fg, master=self.master
        )
        self.btn_home = self.base_btn(
                               text="",
                               position=(20, 20),
                               call=lambda: on_finished("HOME"),
                               icon_gap=0,
                               icon=assets.HOME_ICON(30)
                               )
        self.btn_setting = self.base_btn(
                               text="",
                               position=(mx - bw - 20, 20),
                               call=lambda: on_finished("SETTINGS"),
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
