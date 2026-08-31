import sys
import pygame
from configparser import ConfigParser
from pathlib import Path
from typing import Protocol
from .pages import (
    BaseScene,
    GameScene,
    HelpScene,
    HomeScene,
    SettingsScene,
    SplashScene)


class PathFinder(Protocol):
    def get_map_file(self, level: str, id: int) -> dict[str, Path]:
        ...


class SceneManager:

    def __init__(self,
                 title: str,
                 config: ConfigParser,
                 path_manager: PathFinder) -> None:
        pygame.init()
        self.p_m = path_manager
        self.cfg = config
        self.w = self.get_width(config)
        self.h = self.get_height(config)
        self.screen = pygame.display.set_mode((self.w, self.h))
        self.srect = self.screen.get_rect()
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.title = title
        self.fps = self.cfg.getint("display", "FPS")
        self.bg = pygame.Color(self.cfg.get("color-theme", "COLOR_BG_MAIN"))
        txt_mute = pygame.Color(
            self.cfg.get("color-theme", "COLOR_TEXT_MUTED"))

        self.scenes: dict[str, BaseScene] = {
            "SPLASH": SplashScene(
                self.screen, self.bg, txt_mute,
                self.switch_to, self.cfg),
            "HOME": HomeScene(
                self.screen, self.bg, txt_mute,
                self.switch_to, self.cfg),
            "SETTINGS": SettingsScene(
                self.screen, self.bg, txt_mute,
                self.switch_to, self.cfg, self.p_m),
            "GAME": GameScene(
                self.screen, self.bg, txt_mute,
                self.switch_to, self.cfg
                ),
            "HELP": HelpScene(
                self.screen, self.bg, txt_mute,
                self.switch_to, self.cfg
                ),
        }

        self.current_scene: BaseScene = self.scenes["SPLASH"]

    def _get_dimension(
        self, config: ConfigParser,
        key: str, default: int,
        min_value: int, max_value: int,
            ) -> int:
        if not config:
            return default

        value = config.getint("display", key)

        if value < min_value:
            print(f"[WARNING]: Min {key} = {min_value}")
            return min_value
        if value > max_value:
            print(f"[WARNING]: Max {key} = {max_value}")
            return max_value
        return value

    def get_width(self, config: ConfigParser) -> int:
        return self._get_dimension(config, "width", default=1280,
                                   min_value=900, max_value=1920)

    def get_height(self, config: ConfigParser) -> int:
        return self._get_dimension(config, "height", default=820,
                                   min_value=600, max_value=1080)

    def switch_to(self, scene_name: str) -> None:
        if scene_name == "QUIT":
            self.is_running = False
            return
        if scene_name in self.scenes:
            self.current_scene = self.scenes[scene_name]

    def resize(self, new_width: int, new_height: int) -> None:
        self.w = new_width
        self.h = new_height
        self.screen = pygame.display.set_mode((self.w, self.h))
        self.srect = self.screen.get_rect()

        for scene in self.scenes.values():
            scene.master = self.screen
            scene.on_resize(self.w, self.h)

    def run(self) -> None:
        while self.is_running:
            dt = self.clock.tick(self.fps) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                else:
                    self.current_scene.event_handler(event)
            self.current_scene.update(dt)
            self.current_scene.render(self.screen)
            c_wdt, c_hgt = self.get_width(self.cfg), self.get_height(self.cfg)
            if self.srect.width != c_wdt or self.srect.height != c_hgt:
                self.resize(c_wdt, c_hgt)
            pygame.display.flip()

        pygame.quit()
        sys.exit(0)
