import pygame
from typing import Callable, Any, Optional
from functools import partial
from .base_scene import BaseScene
from ..assets import assets
from configparser import ConfigParser
from ..widget import (
    Button,
    AnimatedText,
    RadioButton,
    RadioGroup,
    Label,
    Spinbox)


class SettingsScene(BaseScene):

    def __init__(self,
                 master: pygame.Surface,
                 bg: pygame.Color,
                 fg: pygame.Color,
                 on_finished: Callable[..., Any],
                 config: Optional[ConfigParser]) -> None:
        super().__init__(master, bg, fg, on_finished, config)
        self.font = assets.BOPS_FONT(35)
        self.font2 = assets.BOPS_FONT(25)
        self.font_title = assets.DIRT_FONT(80)
        self.c_ico = assets.RDO_CHECK_ICON(20)
        self.u_ico = assets.RDO_UNCHEK_ICON(20)
        if self.cfg is not None:
            btn_bg_str = self.cfg.get("color-theme", "COLOR_BTN_DEFAULT")
            bttm_bg_str = self.cfg.get("color-theme", "COLOR_BTN_ACCENT")
            hover_bg_str = self.cfg.get("color-theme", "COLOR_BTN_HOVER")
            unsel_bg_str = self.cfg.get("color-theme", "COLOR_BORDER")
            sel_bg_str = self.cfg.get("color-theme", "COLOR_BTN_ACCENT")
        else:
            btn_bg_str = "grey"
            bttm_bg_str = "darkgrey"
            hover_bg_str = "lightgrey"
            unsel_bg_str = "black"
            sel_bg_str = "white"

        self.btn_bg = pygame.Color(btn_bg_str)
        self.bttm_bg = pygame.Color(bttm_bg_str)
        self.hover_bg = pygame.Color(hover_bg_str)
        self.unsel_bg = pygame.Color(unsel_bg_str)
        self.sel_bg = pygame.Color(sel_bg_str)
        self._build_widget()

    def _build_widget(self) -> None:
        mrect = self.master.get_rect()
        bw, bh = 45, 40
        mx, my = mrect.right, mrect.bottom
        ex, ey = bw + 20, bh + 20

        rbw, espx, nb_rdo = 155, 20, 4
        total_rdo_width = nb_rdo * rbw + (nb_rdo - 1) * espx
        rest_left = (mrect.width - total_rdo_width) // 2
        x_medium = rest_left + rbw + espx
        x_hard = x_medium + rbw + espx
        x_bonus = x_hard + rbw + espx

        self.base_btn = partial(
            Button, text="", width=bw, height=bh, font=self.font,
            bg_color=self.btn_bg, bottom_color=self.bttm_bg,
            hover_color=self.hover_bg, font_color=self.fg, master=self.master
        )
        self.base_rdo = partial(
            RadioButton, width=rbw, height=bh, font=self.font2,
            bg_color=self.btn_bg, bottom_color=self.bttm_bg,
            hover_color=self.hover_bg, selected_color=self.sel_bg,
            unselected_color=self.unsel_bg, font_color=self.fg,
            master=self.master, check_icon=self.c_ico, icon=self.u_ico)
        self.btn_home = self.base_btn(
                                      position=(20, 20),
                                      call=lambda: self.call("HOME"),
                                      icon_gap=0,
                                      icon=assets.HOME_ICON(30)
                                      )
        self.btn_help = self.base_btn(
                               position=(mx - ex, 20),
                               call=lambda: self.call("HELP"),
                               icon_gap=0,
                               icon=assets.HELP_ICON(30)
                               )
        self.btn_save = self.base_btn(
                               position=(mx - ex, my - ey),
                               call=lambda: self.call("HELP"),
                               icon_gap=0,
                               icon=assets.SAVE_ICON(30)
                               )
        self.btn_clear = self.base_btn(
                               position=(mx - ex * 2, my - ey),
                               call=lambda: self.call("HELP"),
                               icon_gap=0,
                               icon=assets.CLEAR_ICON(30)
                               )
        self.btn_cancel = self.base_btn(
                               position=(mx - ex * 3, my - ey),
                               call=lambda: self.call("HELP"),
                               icon_gap=0,
                               icon=assets.CLOSE_ICON(30)
                               )
        self.titre = AnimatedText(
                    self.master, self.font_title,
                    "S E T T I N G", self.fg, 0, -240)
        self.lvl_label = AnimatedText(
                    self.master, self.font, "LEVEL :",
                    self.fg, 0, -110, 0.03)
        self.lvl_value = Label("...", self.font2, self.bg,
                               self.fg, self.master, (0, 0))
        self.map_id = AnimatedText(
                    self.master, self.font, "MAP ID :",
                    self.fg, 0, 20, 0.03)
        self.display = AnimatedText(
                    self.master, self.font, "DISPLAY :",
                    self.fg, 0, 130, 0.03)
        self.easy = self.base_rdo(
            text="EASY", position=(rest_left, 240),
            call=lambda: self.select_level(), value="easy")
        self.medium = self.base_rdo(
            text="MEDIUM", position=(x_medium, 240),
            call=lambda: self.select_level(), value="medium")
        self.hard = self.base_rdo(
            text="HARD", position=(x_hard, 240),
            call=lambda: self.select_level(), value="hard")
        self.challenge = self.base_rdo(
            text="BONUS", position=(x_bonus, 240),
            call=lambda: self.select_level(), value="challenger")
        self.radio_group = RadioGroup()
        self.radio_group.add_radio(self.easy)
        self.radio_group.add_radio(self.medium)
        self.radio_group.add_radio(self.hard)
        self.radio_group.add_radio(self.challenge)
        self.spn = Spinbox(self.font2, self.bg, self.bttm_bg, self.hover_bg,
                           self.fg, self.master, (x_medium, 380))

    def event_handler(self, event: pygame.event.Event) -> None:
        self.radio_group.event_handler()

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
        self.display.update(dt)

        gap = 10
        self.lvl_value.set_pos((
            self.lvl_label.text_rect.right + gap,
            self.lvl_label.text_rect.bottom
        ))
        self.lvl_value.update(dt)

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
        self.display.draw()
        self.lvl_value.draw()
        self.spn.draw()

    def select_level(self) -> None:
        value = self.radio_group.value
        self.lvl_value.set_text(value if value is not None else "")
