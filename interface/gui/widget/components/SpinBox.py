from .BaseWidget import BaseWidget
import pygame
from ...assets import assets
from .Button import Button
from functools import partial
from .Label import Label


class Spinbox(BaseWidget):
    def __init__(self,
                 font: pygame.font.Font,
                 bg_color: pygame.Color,
                 bottom_color: pygame.Color,
                 hover_color: pygame.Color,
                 font_color: pygame.Color,
                 master: pygame.Surface,
                 position: tuple[int, int],
                 default: int = 1,
                 max: int = 2000,
                 min: int = 1,
                 ) -> None:
        super().__init__(font, bg_color, font_color, master)
        self.value = default
        self.min = min
        self.max = max
        self.up_icon = assets.UP_ICON((20, 20))
        self.down_icon = assets.DOWN_ICON((20, 20))
        self.base_btn = partial(
            Button, text="", width=20, height=20,
            font=self.font, bg_color=self.bg, bottom_color=bottom_color,
            hover_color=hover_color, font_color=self.fg,
            master=self.master, elevation=2)
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
        self.val_str = f"{str(self.value).zfill(2)}"
        self.texte = Label(self.val_str, self.font,
                           self.fg, self.bg, self.master, (x, y))

    def draw(self) -> None:
        pygame.draw.rect(self.master, self.fg, self.rect)
        self.down_btn.draw()
        self.up_btn.draw()
        self.texte.draw()

    def update(self, dt: float) -> None:
        pass

    def event_handler(self) -> None:
        pass

    def upgrading(self) -> None:
        if self.value < self.max:
            self.value += 1
            self.val_str = f"{str(self.value).zfill(2)}"
            self.texte.set_text(self.val_str)

    def downgrading(self) -> None:
        if self.value > self.min:
            self.value -= 1
            self.val_str = f"{str(self.value).zfill(2)}"
            self.texte.set_text(self.val_str)
