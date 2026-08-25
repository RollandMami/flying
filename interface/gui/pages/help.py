import pygame
#from ..widget import Button, ProgressBar
#from functools import partial
#from .. import settings
from .base_scene import BaseScene


class HelpScene(BaseScene):

    def __init__(self, master, bg, fg, on_finished):
        super().__init__(master, bg, fg, on_finished)

    def event_handler(self, event: pygame.event.Event) -> None:
        pass

    def update(self, dt: float) -> None:
        pass

    def render(self, surface: pygame.Surface) -> None:
        pass
