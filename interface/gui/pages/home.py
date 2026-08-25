import pygame
from ..widget import Button, AnimatedText
from .base_scene import BaseScene
from typing import Callable, Any
from .. import settings
from ..assets import assets


class HomeScene(BaseScene):
    def __init__(self,
                 master: pygame.Surface,
                 bg: pygame.Color,
                 fg: pygame.Color,
                 on_finished: Callable[..., Any]) -> None:
        super().__init__(master, bg, fg, on_finished)
        self.width, self.height = master.get_width(), master.get_height()
        self.btn_bg = settings.COLOR_BTN_DEFAULT
        self.font = assets.BOPS_FONT(38)
        self.rf = assets.FAST_FONT(38)
        self.font_title = assets.DIRT_FONT(80)
        cx, cy = self.master.get_rect().center
        bw, bh = 260, 45
        ipx, ipy = cx - (bw // 2), cy - (bh // 2)
        e = bh + 20
        self.btn_start = Button("START",
                                bw,
                                bh,
                                self.font,
                                self.btn_bg,
                                self.fg,
                                self.master,
                                (ipx, ipy + e),
                                lambda: on_finished("GAME")
                                )
        self.btn_option = Button("OPTIONS",
                                 bw,
                                 bh,
                                 self.font,
                                 self.btn_bg,
                                 self.fg,
                                 self.master,
                                 (ipx, ipy + e * 2),
                                 lambda: on_finished("SETTINGS")
                                 )
        self.btn_help = Button(
                            "HELP",
                            bw,
                            bh,
                            self.font,
                            self.btn_bg,
                            self.fg,
                            self.master,
                            (ipx, ipy + e * 3),
                            lambda: on_finished("HELP")
                            )
        self.btn_exit = Button(
                            "QUIT",
                            bw,
                            bh,
                            self.rf,
                            self.btn_bg,
                            "red",
                            self.master,
                            (ipx, ipy + e * 4),
                            lambda: pygame.quit()
                            )
        self.titre = AnimatedText(
                    self.master,
                    self.font_title,
                    "H O M E - P A G E",
                    self.fg,
                    0, -100
        )

    def event_handler(self, evt: pygame.event.Event) -> None:
        pass

    def render(self, target: pygame.Surface) -> None:
        target.fill(self.bg)
        self.titre.draw()
        self.btn_start.draw()
        self.btn_option.draw()
        self.btn_help.draw()
        self.btn_exit.draw()

    def update(self, dt: float) -> None:
        self.titre.update(dt)
        self.btn_start.update(dt)
        self.btn_option.update(dt)
        self.btn_help.update(dt)
        self.btn_exit.update(dt)
