
import os
import pygame
from typing import Callable, Any
from configparser import ConfigParser
from .base_scene import BaseScene
from ..widget import Button, AnimatedText
from ..assets import assets
from functools import partial
import warnings
import pygame_gui as pgui
warnings.filterwarnings("ignore", category=UserWarning)


class HelpScene(BaseScene):

    def __init__(self,
                 master: pygame.Surface,
                 bg: pygame.Color,
                 fg: pygame.Color,
                 on_finished: Callable[..., Any],
                 config: ConfigParser) -> None:
        super().__init__(master, bg, fg, on_finished, config)
        self.width, self.height = master.get_width(), master.get_height()
        btn_bg = self.cfg.get("color-theme", "COLOR_BTN_DEFAULT")
        bttm_bg = self.cfg.get("color-theme", "COLOR_BTN_ACCENT")
        hover_bg = self.cfg.get("color-theme", "COLOR_BTN_HOVER")

        self.btn_bg = pygame.Color(btn_bg)
        self.bttm_bg = pygame.Color(bttm_bg)
        self.hover_bg = pygame.Color(hover_bg)
        self.font = assets.BOPS_FONT(15)
        self.font_title = assets.DIRT_FONT(80)
        self.ui_manager = pgui.UIManager((self.width, self.height))
        self._build_widget()

    def _build_widget(self) -> None:
        base = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(base, "help.html"), "r") as f:
            mon_paragraphe = f.read()

        self.texte_box = pgui.elements.UITextBox(
            html_text=mon_paragraphe,
            relative_rect=pygame.Rect((130, 130),
                                      (self.width - 250, self.height - 250)),
            manager=self.ui_manager
        )
        _, cy = self.master.get_rect().center
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
                               call=lambda: self.call("HOME"),
                               icon_gap=0,
                               icon=assets.HOME_ICON(30)
                               )
        self.btn_setting = self.base_btn(
                               text="",
                               position=(mx - bw - 20, 20),
                               call=lambda: self.call("SETTINGS"),
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
        self.ui_manager.process_events(event)

    def update(self, dt: float) -> None:
        self.titre.update(dt)
        self.btn_home.update(dt)
        self.btn_setting.update(dt)
        self.ui_manager.update(dt)

    def render(self, target: pygame.Surface) -> None:
        target.fill(self.bg)
        self.titre.draw()
        self.btn_home.draw()
        self.btn_setting.draw()
        self.ui_manager.draw_ui(target)
