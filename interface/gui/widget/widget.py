from .base_widget import BaseWidget
import pygame
from typing import Callable, Any


class Button(BaseWidget):

    def __init__(self,
                 text: str,
                 width: int,
                 height: int,
                 font: pygame.font.Font,
                 bg_color: str,
                 font_color: str,
                 master: pygame.Surface,
                 position: tuple[int, int],
                 call: Callable[..., Any],
                 elevation: int = 6) -> None:
        super().__init__()
        self._pressed = False
        self._master = master
        self._callable = call
        self._elevation = elevation
        self._dynamic_elv = elevation
        self._oroginal_y = position[1]

        self._top_rect = pygame.Rect(position, (width, height))
        self.bg = bg_color
        self._top_color = self.bg

        self._bottom_rec = pygame.Rect(position, (width, elevation))
        self._bottom_col = "grey"

        self._text = font.render(text, True, font_color)
        self._text_rec = self._text.get_rect(center=self._top_rect.center)

    def draw(self) -> None:
        self.event_handler()

        self._top_rect.y = self._oroginal_y - self._dynamic_elv
        self._text_rec.center = self._top_rect.center
        self._bottom_rec.midtop = self._top_rect.midtop
        self._bottom_rec.height = self._top_rect.height + self._dynamic_elv
        pygame.draw.rect(
            self._master,
            self._bottom_col,
            self._bottom_rec, border_radius=12)
        pygame.draw.rect(
            self._master,
            self._top_color,
            self._top_rect, border_radius=12)
        self._master.blit(self._text, self._text_rec)

    def update(self) -> None:
        pass

    def event_handler(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        if self._top_rect.collidepoint(mouse_pos):
            self._top_color = "red"
            if pygame.mouse.get_pressed()[0]:
                self._dynamic_elv = 0
                self._pressed = True
            else:
                self._dynamic_elv = self._elevation
                if self._pressed:
                    self._callable()
                    self._pressed = False
        else:
            self._top_color = self.bg
