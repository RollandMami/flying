from .BaseWidget import BaseWidget
import pygame
from typing import Callable, Any, Optional
from ...assets import Icon


class Button(BaseWidget):

    def __init__(self,
                 text: str,
                 width: int,
                 height: int,
                 font: pygame.font.Font,
                 bg_color: pygame.Color,
                 bottom_color: pygame.Color,
                 hover_color: pygame.Color,
                 font_color: pygame.Color,
                 master: pygame.Surface,
                 position: tuple[int, int],
                 call: Callable[..., Any],
                 icon: Optional[Icon] = None,
                 icon_gap: int = 5,
                 elevation: int = 6,) -> None:
        super().__init__(font, bg_color, font_color, master)
        self.pressed = False
        self.hover_color = hover_color
        self.callable = call
        self.elevation = elevation
        self.dynamic_elv = elevation
        self.oroginal_y = position[1]

        self.top_rect = pygame.Rect(position, (width, height))
        self.top_color = self.bg

        self.bottom_rec = pygame.Rect(position, (width, elevation))
        self.bottom_col = bottom_color

        self.text = font.render(text, True, self.fg)

        self.icon = icon.surface if icon else None

        if self.icon:
            gap = icon_gap
            total_w = self.icon.get_width() + gap + self.text.get_width()
            start_x = self.top_rect.centerx - total_w // 2

            self.text_rec = self.text.get_rect(
                midleft=(start_x, self.top_rect.centery))

            self.icon_rec = self.icon.get_rect(
                midleft=(self.text_rec.right + gap, self.top_rect.centery)
            )
        else:
            self.icon = None
            self.text_rec = self.text.get_rect(center=self.top_rect.center)

    def draw(self) -> None:
        self.event_handler()

        self.top_rect.y = self.oroginal_y - self.dynamic_elv

        if self.icon:
            self.text_rec.centery = self.top_rect.centery
            self.icon_rec.centery = self.top_rect.centery
        else:
            self.text_rec.center = self.top_rect.center

        self.bottom_rec.midtop = self.top_rect.midtop
        self.bottom_rec.height = self.top_rect.height + self.dynamic_elv
        pygame.draw.rect(
            self.master,
            self.bottom_col,
            self.bottom_rec, border_radius=12)
        pygame.draw.rect(
            self.master,
            self.top_color,
            self.top_rect, border_radius=12)
        self.master.blit(self.text, self.text_rec)
        if self.icon:
            self.master.blit(self.icon, self.icon_rec)

    def update(self, dt: float) -> None:
        pass

    def event_handler(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = self.hover_color
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elv = 0
                self.pressed = True
            else:
                self.dynamic_elv = self.elevation
                if self.pressed:
                    self.callable()
                    self.pressed = False
        else:
            self.top_color = self.bg
