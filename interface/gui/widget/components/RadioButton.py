from .Button import Button
import pygame
from typing import Callable, Any, Optional
from ...assets import Icon


class RadioButton(Button):

    def __init__(self,
                 text: str,
                 width: int,
                 height: int,
                 font: pygame.font.Font,
                 bg_color: pygame.Color,
                 bottom_color: pygame.Color,
                 hover_color: pygame.Color,
                 selected_color: pygame.Color,
                 unselected_color: pygame.Color,
                 font_color: pygame.Color,
                 master: pygame.Surface,
                 position: tuple[int, int],
                 call: Callable[..., Any],
                 value: str,
                 check_icon: Optional[Icon],
                 icon: Optional[Icon],
                 icon_gap: int = 5,
                 elevation: int = 6,
                 ) -> None:
        super().__init__(text, width, height, font,
                         bg_color, bottom_color, hover_color,
                         font_color, master, position, call,
                         icon, icon_gap, elevation)
        self.bottom_col = unselected_color
        self.unsel_color = unselected_color
        self.sel_color = selected_color
        self.value = value
        self.is_selected = False
        self.check_icon = check_icon.surface if check_icon else None
        self.default_icon = icon.surface if icon else None

    def update(self, dt: float) -> None:
        super().update(dt)
        if self.is_selected:
            self.icon = self.check_icon
            self.bottom_col = self.sel_color
        else:
            self.icon = self.default_icon
            self.bottom_col = self.unsel_color
