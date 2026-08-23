import sys
import pygame
from .pages.base_scene import BaseScene
# from .pages.game_scene import GameScene
# from .pages.help_scene import HelpScene
# from .pages.home_scene import HomeScene
# from .pages.settings_scene import SettingsScene
from .pages.splash import SplashScene


class SceneManager:

    def __init__(self, w: int, h: int, title: str) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((w, h))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.w = w
        self.h = h
        self.title = title

        self.scenes: dict[str, BaseScene] = {
            "SPLASH": SplashScene(master=self.screen, bg="red"),
            # "HOME": HomeScene(self),
            # "SETTINGS": SettingsScene(self),
            # "GAME": GameScene(self),
            # "HELP": HelpScene(self),
        }

        self.current_scene: BaseScene = self.scenes["SPLASH"]

    def switch_to(self, scene_name: str) -> None:
        """Change la scène active."""
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