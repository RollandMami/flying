import pygame
#from ..widget import Button
#from .. import settings
from .base_scene import BaseScene


class GameScene(BaseScene):

    def __init__(self, master, bg, fg, on_finished):
        super().__init__(master, bg, fg, on_finished)

    def event_handler(self, event: pygame.event.Event) -> None:
        pass

    def update(self, dt: float) -> None:
        pass

    def render(self, target: pygame.Surface) -> None:
        pass
