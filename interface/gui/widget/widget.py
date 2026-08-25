from .base_widget import BaseWidget
import pygame
from typing import Callable, Any, Optional
from .. import settings
from ..assets import Icon


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
                 icon: Optional[Icon] = None,
                 icon_gap: int = 10,
                 elevation: int = 6,) -> None:
        super().__init__(font, bg_color, font_color, master)
        self.pressed = False
        self.hover_color = settings.COLOR_BTN_HOVER
        self.callable = call
        self.elevation = elevation
        self.dynamic_elv = elevation
        self.oroginal_y = position[1]

        self.top_rect = pygame.Rect(position, (width, height))
        self.top_color = self.bg

        self.bottom_rec = pygame.Rect(position, (width, elevation))
        self.bottom_col = settings.COLOR_BTN_ACCENT

        self.text = font.render(text, True, self.fg)

        self.icon = icon.surface if icon else None

        if self.icon:
            gap = icon_gap
            total_w = self.icon.get_rect() + gap + self.text.get_width()
            start_x = self.top_rect.centerx - total_w // 2

            self.icon_rec = self.icon.get_rect(
                midleft=(start_x, self.top_rect.centery)
            )
            self.text_rec = self.text.get_rect(
                midleft=(self.icon_rec.right + gap, self.top_rect.centery))
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
        if self.icon:
            self.master.blit(self.icon, self.icon_rec)
        self.master.blit(self.text, self.text_rec)

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


class ProgressBar(BaseWidget):

    def __init__(
        self,
        bg: pygame.Color,
        font: pygame.font.Font,
        fg: pygame.Color,
        master: pygame.Surface,
        position: tuple[int, int],
        height: int = 25,
        width: int | None = None,
        duration: float = 2.0,
    ) -> None:
        super().__init__(font, bg, fg, master)
        self.duration = duration
        self.elapsed = 0.0
        if not width:
            width = self.master.get_width() - 20
        self.out_rect = pygame.Rect(position, (width, height))
        x, y = position[0] + 2, position[1] + 2
        self.inner_max_width = width - 4
        self.inner_rect = pygame.Rect((x, y), (0, height - 4))
        self.text1 = self.font.render("Loading ...", True, self.fg)
        self.text1_rec = self.text1.get_rect(center=self.inner_rect.center)
        self.text2 = self.font.render("0.0 %", True, self.fg)
        self.text2_rec = self.text1.get_rect(center=self.inner_rect.center)

    @property
    def is_finished(self) -> bool:
        return self.elapsed >= self.duration

    def update(self, dt: float) -> None:
        if self.is_finished:
            return
        self.elapsed = min(self.duration, self.elapsed + dt)
        progress = self.elapsed / self.duration
        self.text2 = self.font.render(f"{progress * 100:.1f} %", True, self.fg)
        self.inner_rect.width = int(self.inner_max_width * progress)

    def draw(self) -> None:
        self.text1_rec.left = self.inner_rect.left + 7
        self.text2_rec.right = self.out_rect.right + 7
        pygame.draw.rect(self.master, self.bg, self.out_rect)
        pygame.draw.rect(self.master, "blue", self.inner_rect)
        self.master.blit(self.text1, self.text1_rec)
        self.master.blit(self.text2, self.text2_rec)

    def event_handler(self) -> None:
        pass


class AnimatedText(BaseWidget):

    def __init__(self,
                 master: pygame.Surface,
                 font: pygame.font.Font,
                 texte: str,
                 color: pygame.Color,
                 dx: int = 0,
                 dy: int = 0,
                 delay: float = 0.05) -> None:
        super().__init__(font, "grey", color, master)
        self.str = texte

        self.char_delay = delay
        self.elapsed = 0.0
        self.index = 0
        self.dx, self.dy = dx, dy

        self.text = self.font.render("", True, self.fg)
        cx, cy = self.master.get_rect().center
        self.text_rect = self.text.get_rect(
            center=(cx + self.dx, cy + self.dy)
        )

    def draw(self) -> None:
        cx, cy = self.master.get_rect().center
        self.text_rect.center = (cx + self.dx, cy + self.dy)
        self.master.blit(self.text, self.text_rect)

    @property
    def is_finished(self) -> bool:
        return self.index >= len(self.str)

    def update(self, dt: float) -> None:
        if self.is_finished:
            return

        self.elapsed += dt
        while (
            self.elapsed >= self.char_delay and
            self.index < len(self.str)
        ):
            self.elapsed -= self.char_delay
            self.index += 1
            current_text = self.str[:self.index]
            self.text = self.font.render(
                current_text,
                True,
                self.fg
            )
            cx, cy = self.master.get_rect().center
            self.text_rect = self.text.get_rect(
                center=(cx + self.dx, cy + self.dy)
            )

    def event_handler(self) -> None:
        pass


class Grid(BaseWidget):

    def __init__(self) -> None:
        ...

    def draw(self) -> None:
        ...

    def update(self, dt: float) -> None:
        ...

    def event_handler(self) -> None:
        ...
