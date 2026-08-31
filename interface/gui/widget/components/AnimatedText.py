from .BaseWidget import BaseWidget
import pygame


class AnimatedText(BaseWidget):

    def __init__(self,
                 master: pygame.Surface,
                 font: pygame.font.Font,
                 texte: str,
                 color: pygame.Color,
                 dx: int = 0,
                 dy: int = 0,
                 delay: float = 0.05) -> None:
        super().__init__(font, pygame.Color("grey"), color, master)
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

    @property
    def bottom(self) -> int:
        return self.text_rect.bottom

    @property
    def top(self) -> int:
        return self.text_rect.top

    @property
    def right(self) -> int:
        return self.text_rect.right

    @property
    def rect(self) -> pygame.Rect:
        return self.text_rect

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
