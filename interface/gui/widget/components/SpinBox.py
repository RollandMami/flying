from .BaseWidget import BaseWidget
import pygame
from typing import Optional
from ...assets import assets
from .Button import Button
from functools import partial
from .Label import Label
from math import inf


class Spinbox(BaseWidget):
    def __init__(self,
                 font: pygame.font.Font,
                 bg_color: pygame.Color,
                 font_color: pygame.Color,
                 master: pygame.Surface,
                 position: tuple[int, int],
                 max: Optional[int] = inf,
                 min: Optional[int] = 1,
                 ) -> None:
        super().__init__(font, bg_color, font_color, master)
        self.value = min
        self.min = min
        self.max = max
        self.up_icon = assets.UP_ICON((20, 20))
        self.down_icon = assets.DOWN_ICON((20, 20))
        self.base_btn = partial(
            Button, text="", width=20, height=20,
            font=self.font, bg_color=self.bg,
            font_color=self.fg, master=self.master, elevation=2)
        self.up_btn = self.base_btn(
            position=position, call=lambda: self.upgrading(),
            icon=self.up_icon
        )
        x1, y1 = position
        y1 += 20
        self.down_btn = self.base_btn(
            position=(x1, y1), call=lambda: self.downgrading(),
            icon=self.down_icon
        )
        x_rect, y_rect = position
        x_rect += 20
        self.rect = pygame.Rect(x_rect, y_rect, 80, 40)

        x = self.rect.centerx - 20
        y = self.rect.bottom - 4
        self.val_str = f"{self.value:02d}"
        self.texte = Label(self.val_str, self.font,
                           self.fg, self.bg, self.master, (x, y))

    def draw(self):
        pygame.draw.rect(self.master, self.fg, self.rect)
        self.down_btn.draw()
        self.up_btn.draw()
        self.texte.draw()

    def update(self):
        return super().update()

    def event_handler(self):
        return super().event_handler()

    def upgrading(self) -> None:
        if self.value < self.max:
            self.value += 1
            self.val_str = f"{self.value:02d}"
            self.texte.set_text(self.val_str)

    def downgrading(self)-> None:
        if self.value > self.min:
            self.value -= 1
            self.val_str = f"{self.value:02d}"
            self.texte.set_text(self.val_str)
