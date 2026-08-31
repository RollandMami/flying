import pygame
from .base_scene import BaseScene
from typing import Callable, Any
from ..assets import assets
from configparser import ConfigParser
from functools import partial
from ..widget import (
    Button,
    AnimatedText,
    Label,
    LevelShower)


class HomeScene(BaseScene):
    def __init__(self,
                 master: pygame.Surface,
                 bg: pygame.Color,
                 fg: pygame.Color,
                 on_finished: Callable[..., Any],
                 config: ConfigParser) -> None:
        super().__init__(master, bg, fg, on_finished, config)
        btn_bg_str = self.cfg.get("color-theme", "COLOR_BTN_DEFAULT")
        bttm_bg_str = self.cfg.get("color-theme", "COLOR_BTN_ACCENT")
        hover_bg_str = self.cfg.get("color-theme", "COLOR_BTN_HOVER")
        self.level = self.cfg.get("level", "stage").upper()
        self.btn_bg = pygame.Color(btn_bg_str)
        self.bttm_bg = pygame.Color(bttm_bg_str)
        self.hover_bg = pygame.Color(hover_bg_str)
        self.font = assets.BOPS_FONT(38)
        self.font2 = assets.BOPS_FONT(25)
        self.font3 = assets.BOPS_FONT(20)
        self.rf = assets.FAST_FONT(38)
        self.font_title = assets.DIRT_FONT(80)

        self._build_widget()

    def _build_widget(self) -> None:
        self.mrect = self.master.get_rect()
        self.width, self.height = self.mrect.width, self.mrect.height
        cx, cy = self.mrect.center
        bw, bh = 260, 45
        ipx, ipy = cx - (bw // 2), cy - (bh // 2)
        e = bh + 20
        wi = 30

        map_id = self.cfg.getint("level", "map_id")
        self.map_id = f"MAP ID: {str(map_id).zfill(2)}"
        self.base_btn = partial(
            Button, width=bw, height=bh, font=self.font, bg_color=self.btn_bg,
            bottom_color=self.bttm_bg, hover_color=self.hover_bg,
            font_color=self.fg, master=self.master
        )
        self.btn_start = self.base_btn(
                                text="START",
                                position=(ipx, ipy + e),
                                call=lambda: self.call("GAME"),
                                icon=assets.START_ICON(wi+10)
                                )
        self.btn_option = self.base_btn(
                                text="OPTIONS",
                                position=(ipx, ipy + e * 2),
                                call=lambda: self.call("SETTINGS"),
                                icon=assets.SETTING_ICON(wi)
                                 )
        self.btn_help = self.base_btn(
                            text="HELP",
                            position=(ipx, ipy + e * 3),
                            call=lambda: self.call("HELP"),
                            icon=assets.HELP_ICON(wi)
                            )
        self.btn_exit = Button(
                            "QUIT", bw, bh, self.rf, self.btn_bg, self.bttm_bg,
                            self.hover_bg, "red", self.master,
                            (ipx, ipy + e * 4), lambda: self.call("QUIT"),
                            icon=assets.LOUT_ICON(wi))
        self.titre = AnimatedText(
                    self.master,
                    self.font_title,
                    "H O M E - P A G E",
                    self.fg,
                    0, -90
        )
        self.lvl_map_id = Label(self.map_id, self.font2, self.bg,
                                self.fg, self.master, (self.width - 150, 40))
        self.lvl_show = LevelShower(self.font3, self.fg, self.bg,
                                    self.master, (20, 10), self.level)

    def _set_map_id(self, id: int) -> None:
        if id >= 1 and id <= 3:
            self.map_id = f"MAP ID: {str(id).zfill(2)}"

    def event_handler(self, evt: pygame.event.Event) -> None:
        pass

    def render(self, target: pygame.Surface) -> None:
        target.fill(self.bg)
        self.titre.draw()
        self.btn_start.draw()
        self.btn_option.draw()
        self.btn_help.draw()
        self.btn_exit.draw()
        self.lvl_map_id.draw()
        self.lvl_show.draw()

    def update(self, dt: float) -> None:
        super().update(dt)
        self.titre.update(dt)
        self.btn_start.update(dt)
        self.btn_option.update(dt)
        self.btn_help.update(dt)
        self.btn_exit.update(dt)
        self.lvl_map_id.update(dt)
        self.lvl_show.update(dt)
        curr_lvl = self.cfg.get("level", "stage").upper()
        curr_map_id = self.cfg.getint("level", "map_id")
        curr_map_id = f"MAP ID: {str(curr_map_id).zfill(2)}"
        if self.level != curr_lvl:
            self.level = curr_lvl
            self.lvl_show.set_level(curr_lvl)
        if self.map_id != curr_map_id:
            self.map_id = curr_map_id
            self.lvl_map_id.set_text(curr_map_id)
