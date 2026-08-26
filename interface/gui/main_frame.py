import sys
import pygame
from . import settings
from .pages import (
    BaseScene,
    GameScene,
    HelpScene,
    HomeScene,
    SettingsScene,
    SplashScene)


class SceneManager:

    def __init__(self, w: int, h: int, title: str) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((w, h))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.w = w
        self.h = h
        self.bg = settings.COLOR_BG_MAIN
        txt_mute = settings.COLOR_TEXT_MUTED
        self.title = title

        self.scenes: dict[str, BaseScene] = {
            "SPLASH": SplashScene(
                self.screen, self.bg, txt_mute,
                self.switch_to),
            "HOME": HomeScene(
                self.screen, self.bg, txt_mute,
                self.switch_to),
            "SETTINGS": SettingsScene(
                self.screen, self.bg, txt_mute,
                self.switch_to),
            "GAME": GameScene(
                self.screen, self.bg, txt_mute,
                self.switch_to
                ),
            "HELP": HelpScene(
                self.screen, self.bg, txt_mute,
                self.switch_to
                ),
        }

        self.current_scene: BaseScene = self.scenes["SPLASH"]

    def switch_to(self, scene_name: str) -> None:
        """Change la scène active."""
        if scene_name == "QUIT":
            self.is_running = False
            return
        if scene_name in self.scenes:
            self.current_scene = self.scenes[scene_name]

    def run(self) -> None:
        while self.is_running:
            dt = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                else:
                    self.current_scene.event_handler(event)
            self.current_scene.update(dt)
            self.current_scene.render(self.screen)
            pygame.display.flip()

        pygame.quit()
        sys.exit(0)
