from .BaseWidget import BaseWidget
import pygame
from typing import Optional
from ...assets import assets
from .Button import Button
from functools import partial
from .Label import Label


class Spinbox(BaseWidget):
    def __init__(self,
                 font: pygame.font.Font,
                 bg_color: pygame.Color,
                 font_color: pygame.Color,
                 master: pygame.Surface,
                 position: tuple[int, int],
                 max: Optional[int],
                 min: Optional[int] = 0,
                 ) -> None:
        super().__init__(font, bg_color, font_color, master)
        self.value = min
        self.up_icon = assets.UP_ICON(10, 15)
        self.down_icon = assets.DOWN_ICON(10, 15)
        self.base_btn = partial(
            Button, text="", width=10, height=15,
            font=self.font, bg_color=self.bg,
            font_color=self.fg, master=self.master, elevation=2)
        self.up_btn = self.base_btn(
            position=position, call=lambda: print("uppering"),
            icon=self.up_icon
        )
        self.down_btn = self.base_btn(
            position=(position[0], 15), call=lambda: print("downgrade"),
            icon=self.down_icon
        )
        x_rect, y_rect = position
        x_rect += 10
        self.rect = pygame.Rect(x_rect, y_rect, 80, 30)

        x = self.rect.left
        self.texte = Label(self.value, self.font,
                           self.bg, self.fg, self.master, (x, 12))

    def draw(self):
        self.down_btn.draw()
        self.up_btn.draw()
        self.texte.draw()

    def update(self):
        return super().update()

    def event_handler(self):
        return super().event_handler()
