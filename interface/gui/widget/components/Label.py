from .BaseWidget import BaseWidget
import pygame


class Label(BaseWidget):
    VALID_ANCHORS = {
        "topleft", "topright", "bottomleft", "bottomright",
        "midtop", "midbottom", "midleft", "midright",
        "center",
    }

    def __init__(self,
                 text: str,
                 font: pygame.font.Font,
                 bg_color: pygame.Color,
                 font_color: pygame.Color,
                 master: pygame.Surface,
                 position: tuple[int, int],
                 anchor: str | None = None) -> None:
        super().__init__(font, bg_color, font_color, master)
        self.label = text
        self.position = position
        self.anchor = self._validate_anchor(anchor)

        self.set_text(text)

    def _validate_anchor(self, anchor: str | None) -> str:
        anchor = anchor or "bottomleft"
        if anchor not in self.VALID_ANCHORS:
            raise ValueError(f"invalid anchor: {anchor!r}")
        return anchor

    def set_pos(self, pos: tuple[int, int]) -> None:
        self.position = pos
        setattr(self.text_rect, self.anchor, self.position)

    def set_text(self, text: str) -> None:
        self.label = text
        self.text = self.font.render(self.label, True, self.fg, self.bg)
        self.text_rect = self.text.get_rect(**{self.anchor: self.position})

    def event_handler(self) -> None:
        pass

    def update(self, dt: float) -> None:
        pass

    def draw(self) -> None:
        self.master.blit(self.text, self.text_rect)
