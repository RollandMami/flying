from .BaseWidget import BaseWidget
import pygame
from typing import Optional
from ...assets import assets
from .Label import Label


class LevelShower(BaseWidget):
    def __init__(self,
                 font: pygame.font.Font,
                 bg_color: pygame.Color,
                 font_color: pygame.Color,
                 master: pygame.Surface,
                 position: tuple[int, int],
                 level: Optional[str]) -> None:
        super().__init__(font, bg_color, font_color, master)
        wi = 70
        self.icons = {
            "EASY": assets.EASY_ICON(wi),
            "MEDIUM": assets.MEDIUM_ICON(wi),
            "HARD": assets.HARD_ICON(wi),
            "CHALLENGER": assets.IMPOSSIBLE_ICON(wi)
        }

        self.width = 217
        self.height = 90
        self.level = level.upper() if level is not None else 'EASY'
        self.default_icon = self.icons.get(
            self.level, self.icons["EASY"]).surface
        self.current_icon = self.default_icon

        topleft = position[0], position[1]
        self.circle_rect = pygame.Rect(topleft, (90, 90))
        self.icon_rect = self.current_icon.get_rect(
            center=self.circle_rect.center
        )

        x, y = position
        x_rect = x + 90 - 3
        y_rect = y + 30
        self.rect = pygame.Rect(x_rect, y_rect, 100, 30)
        txt_x, txt_y = self.rect.left + 6, self.rect.bottom - 1
        self.lvl_value = Label(
            self.level, self.font, self.bg,
            self.fg, self.master, (txt_x, txt_y))
        d = 90
        x1 = x + d - 3 + 100
        y1 = y + 30
        self.points = [
            (x1, y1),
            (x1 + 30, y1),
            (x1, y1 + 30)
        ]

    def draw(self) -> None:
        pygame.draw.rect(self.master, self.bg, self.rect)
        pygame.draw.circle(self.master, self.bg,
                           self.circle_rect.center, 45, 5)
        self.master.blit(self.current_icon, self.icon_rect)
        pygame.draw.polygon(self.master, self.bg, self.points)
        self.lvl_value.draw()

    def update(self, dt: float) -> None:
        pass

    def event_handler(self) -> None:
        pass

    def set_level(self, level: str) -> None:
        level = level.upper()
        if level not in self.icons.keys():
            raise ValueError("LEVEL ERROR")
        self.current_icon = self.icons.get(level, self.icons["EASY"]).surface
        self.lvl_value.set_text(level)
        self.level = level
        self.draw()
