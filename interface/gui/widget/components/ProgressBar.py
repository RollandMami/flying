from .BaseWidget import BaseWidget
import pygame


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
