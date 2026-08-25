from .base_widget import BaseWidget
import pygame
from typing import Callable, Any
from .. import settings


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
                 elevation: int = 6,
                 icon) -> None:
        super().__init__(font, bg_color, font_color, master)
        self._pressed = False
        self.master = master
        self.hover_color = settings.COLOR_BTN_HOVER
        self._callable = call
        self._elevation = elevation
        self._dynamic_elv = elevation
        self._oroginal_y = position[1]

        self._top_rect = pygame.Rect(position, (width, height))
        self._top_color = self.bg

        self._bottom_rec = pygame.Rect(position, (width, elevation))
        self._bottom_col = settings.COLOR_BTN_ACCENT

        self._text = font.render(text, True, self.fg)
        self._text_rec = self._text.get_rect(center=self._top_rect.center)

    def draw(self) -> None:
        self.event_handler()

        self._top_rect.y = self._oroginal_y - self._dynamic_elv
        self._text_rec.center = self._top_rect.center
        self._bottom_rec.midtop = self._top_rect.midtop
        self._bottom_rec.height = self._top_rect.height + self._dynamic_elv
        pygame.draw.rect(
            self.master,
            self._bottom_col,
            self._bottom_rec, border_radius=12)
        pygame.draw.rect(
            self.master,
            self._top_color,
            self._top_rect, border_radius=12)
        self.master.blit(self._text, self._text_rec)

    def update(self, dt: float) -> None:
        pass

    def event_handler(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        if self._top_rect.collidepoint(mouse_pos):
            self._top_color = self.hover_color
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
        self._duration = duration
        self._elapsed = 0.0
        if not width:
            width = self.master.get_width() - 20
        self._out_rect = pygame.Rect(position, (width, height))
        x, y = position[0] + 2, position[1] + 2
        self._inner_max_width = width - 4
        self._inner_rect = pygame.Rect((x, y), (0, height - 4))
        self.text1 = self.font.render("Loading ...", True, self.fg)
        self.text1_rec = self.text1.get_rect(center=self._inner_rect.center)
        self.text2 = self.font.render("0.0 %", True, self.fg)
        self.text2_rec = self.text1.get_rect(center=self._inner_rect.center)

    @property
    def is_finished(self) -> bool:
        return self._elapsed >= self._duration

    def update(self, dt: float) -> None:
        if self.is_finished:
            return
        self._elapsed = min(self._duration, self._elapsed + dt)
        progress = self._elapsed / self._duration
        self.text2 = self.font.render(f"{progress * 100:.1f} %", True, self.fg)
        self._inner_rect.width = int(self._inner_max_width * progress)

    def draw(self) -> None:
        self.text1_rec.left = self._inner_rect.left + 7
        self.text2_rec.right = self._out_rect.right + 7
        pygame.draw.rect(self.master, self.bg, self._out_rect)
        pygame.draw.rect(self.master, "blue", self._inner_rect)
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

        self._char_delay = delay
        self._elapsed = 0.0
        self._index = 0
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
        return self._index >= len(self.str)

    def update(self, dt: float) -> None:
        if self.is_finished:
            return

        self._elapsed += dt
        while (
            self._elapsed >= self._char_delay and
            self._index < len(self.str)
        ):
            self._elapsed -= self._char_delay
            self._index += 1
            current_text = self.str[:self._index]
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
