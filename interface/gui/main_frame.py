import pygame
import sys
from .widget import Button
from functools import partial
from . import settings


class Window:

    def __init__(self,
                 bg: pygame.Color,
                 title: str,
                 w: int,
                 h: int) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((w, h))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.isrunning = True
        self.bg = bg
        self.font = pygame.font.Font(None, 16)
        self.AppButton = partial(
                            Button,
                            width=80,
                            height=25,
                            font=self.font,
                            bg_color=settings.COLOR_BTN_DEFAULT,
                            font_color=settings.COLOR_TEXT_PRIMARY,
                            master=self.screen,
                            elevation=4)
        self.btn_test = self.AppButton(
            text="test",
            position=(200, 200),
            call=lambda: print("hello world"),
        )

    def handle_event(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(1)

    def render(self) -> None:
        self.screen.fill(self.bg)
        self.btn_test.draw()

    def update(self) -> None:
        pygame.display.flip()

    def run(self) -> None:
        while self.isrunning:
            self.handle_event()
            self.render()
            self.update()
            self.clock.tick(60)
        pygame.quit()
        sys.exit(1)
