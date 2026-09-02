import pygame
from pathlib import Path
from typing import Protocol
from typing import Callable, Any
from configparser import ConfigParser
from functools import partial
from .base_scene import BaseScene
from ..assets import assets
from ..widget import (
    Button,
    AnimatedText,
    Grid)
from infrastructure import TxtParser


class PathFinder(Protocol):
    def get_map_file(self, level: str, id: int) -> dict[str, Path]:
        ...


class GameScene(BaseScene):

    def __init__(self,
                 master: pygame.Surface,
                 bg: pygame.Color,
                 fg: pygame.Color,
                 on_finished: Callable[..., Any],
                 config: ConfigParser,
                 p_m: PathFinder,
                 t_parser: TxtParser) -> None:
        super().__init__(master, bg, fg, on_finished, config)
        btn_bg = self.cfg.get("color-theme", "COLOR_BTN_DEFAULT")
        bttm_bg = self.cfg.get("color-theme", "COLOR_BTN_ACCENT")
        hover_bg = self.cfg.get("color-theme", "COLOR_BTN_HOVER")

        self.btn_bg = pygame.Color(btn_bg)
        self.bttm_bg = pygame.Color(bttm_bg)
        self.hover_bg = pygame.Color(hover_bg)
        self.font = assets.BOPS_FONT(15)
        self.font_title = assets.DIRT_FONT(80)
        self.t_parser = t_parser
        self.p_m = p_m

        self._build_widget()

    def _build_widget(self):
        mrect = self.master.get_rect()
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
                               call=lambda: self.call("HOME"),
                               icon_gap=0,
                               icon=assets.HOME_ICON(30)
                               )
        self.btn_setting = self.base_btn(
                               text="",
                               position=(20 + bw + 20, my),
                               call=lambda: self.call("SETTINGS"),
                               icon_gap=0,
                               icon=assets.SETTING_ICON(30)
                               )
        self.titre = AnimatedText(
                    self.master, self.font_title,
                    "R E A D Y", self.fg, 0, 0
        )
        self.grid = Grid(None, self.bg, self.fg, self.master, (80, 80), 40)
        self.level = self.cfg.get("level", "stage")
        self.map_id = self.cfg.getint("level", "map_id")
        self.map_file = self.p_m.get_map_file(self.level, self.map_id)
        self.map_data = self.t_parser.load(list(self.map_file.values())[0])
        print(str(self.map_data))

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
