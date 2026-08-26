import pygame
from .. import settings
from typing import Callable, Any
from functools import partial
from .base_scene import BaseScene
from ..assets import assets
from ..widget import (
    Button,
    AnimatedText,
    RadioButton,)
# RadioGroup)


class SettingsScene(BaseScene):

    def __init__(self,
                 master: pygame.Surface,
                 bg: pygame.Color,
                 fg: pygame.Color,
                 on_finished: Callable[..., Any]):
        super().__init__(master, bg, fg, on_finished)
        self.btn_bg = settings.COLOR_BTN_DEFAULT
        self.font = assets.BOPS_FONT(35)
        self.font2 = assets.BOPS_FONT(25)
        self.font_title = assets.DIRT_FONT(80)
        mrect = self.master.get_rect()
        bw, bh = 45, 40
        rbw = bw + 130
        mx, my = mrect.right, mrect.bottom
        ex, ey = bw + 20, bh + 20
        self.c_ico = assets.RDO_CHECK_ICON(20)
        self.u_ico = assets.RDO_UNCHEK_ICON(20)
        self.base_btn = partial(
            Button,
            text="",
            width=bw,
            height=bh,
            font=self.font,
            bg_color=self.btn_bg,
            font_color=self.fg,
            master=self.master)
        self.base_rdo = partial(
            RadioButton,
            width=rbw,
            height=bh,
            font=self.font2,
            bg_color=self.btn_bg,
            font_color=self.fg,
            master=self.master,
            check_icon=self.c_ico,
            icon=self.u_ico
            )
        self.btn_home = self.base_btn(
                                      position=(20, 20),
                                      call=lambda: on_finished("HOME"),
                                      icon_gap=0,
                                      icon=assets.HOME_ICON(30)
                                      )
        self.btn_help = self.base_btn(
                               position=(mx - ex, 20),
                               call=lambda: on_finished("HELP"),
                               icon_gap=0,
                               icon=assets.HELP_ICON(30)
                               )
        self.btn_save = self.base_btn(
                               position=(mx - ex, my - ey),
                               call=lambda: on_finished("HELP"),
                               icon_gap=0,
                               icon=assets.SAVE_ICON(30)
                               )
        self.btn_clear = self.base_btn(
                               position=(mx - ex * 2, my - ey),
                               call=lambda: on_finished("HELP"),
                               icon_gap=0,
                               icon=assets.CLEAR_ICON(30)
                               )
        self.btn_cancel = self.base_btn(
                               position=(mx - ex * 3, my - ey),
                               call=lambda: on_finished("HELP"),
                               icon_gap=0,
                               icon=assets.CLOSE_ICON(30)
                               )
        self.titre = AnimatedText(
                    self.master, self.font_title,
                    "S E T T I N G", self.fg, 0, -160)
        self.lvl_label = AnimatedText(
                    self.master, self.font, "LEVEL :",
                    self.fg, -150, -70, 0.03)
        self.map_id = AnimatedText(
                    self.master, self.font, "MAP ID :",
                    self.fg, -143, 60, 0.03)
        self.easy = self.base_rdo(
            text="EASY", position=(50, 50), call=lambda: print("EASY"),
            value="easy")
        self.medium = self.base_rdo(
            text="MEDIUM", position=(50 + rbw + 20, 50), call=lambda: print("MEDIUM"),
            value="medium")
        self.hard = self.base_rdo(
            text="HARD", position=(0 + rbw + 40, 50), call=lambda: print("HARD"),
            value="hard")
        self.challenge = self.base_rdo(
            text="CHALLENGE", position=(0 + rbw + 60, 50), call=lambda: print("CHALLENGE"),
            value="challenge")

    def event_handler(self, event: pygame.event.Event) -> None:
        pass

    def update(self, dt: float) -> None:
        self.titre.update(dt)
        self.lvl_label.update(dt)
        self.map_id.update(dt)
        self.btn_home.update(dt)
        self.btn_help.update(dt)
        self.btn_save.update(dt)
        self.btn_clear.update(dt)
        self.btn_cancel.update(dt)
        self.easy.update(dt)
        self.medium.update(dt)
        self.hard.update(dt)
        self.challenge.update(dt)

    def render(self, target: pygame.Surface) -> None:
        target.fill(self.bg)
        self.titre.draw()
        self.lvl_label.draw()
        self.map_id.draw()
        self.btn_home.draw()
        self.btn_help.draw()
        self.btn_save.draw()
        self.btn_clear.draw()
        self.btn_cancel.draw()
        self.easy.draw()
        self.medium.draw()
        self.hard.draw()
        self.challenge.draw()
