from .BaseWidget import BaseWidget
import pygame


class Label(BaseWidget):
    def __init__(self,
                 text: str,
                 font: pygame.font.Font,
                 bg_color: pygame.Color,
                 font_color: pygame.Color,
                 master: pygame.Surface,
                 position: tuple[int, int]) -> None:
        super().__init__(font, bg_color, font_color, master)
        self.label = text
        self.position = position

        self.text = self.font.render(self.label, True, self.fg, self.bg)
        self.text_rect = self.text.get_rect(bottomleft=self.position)

    def set_pos(self, pos: tuple[int, int]) -> None:
        self.position = pos
        self.text_rect.bottomleft = self.position

    def set_text(self, text: str) -> None:
        self.label = text
        self.text = self.font.render(self.label, True, self.fg, self.bg)
        self.text_rect = self.text.get_rect(bottomleft=self.position)

    def event_handler(self) -> None:
        pass

    def update(self, dt: float) -> None:
        pass

    def draw(self) -> None:
        self.master.blit(self.text, self.text_rect)
