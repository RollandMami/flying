import pygame
from functools import partial
import os

bpath = "/".join(os.path.abspath(__file__).split("/")[:-1])


class Font:
    _cache: dict[tuple[str, int], pygame.font.Font] = {}

    def __new__(cls, path: str, size: int) -> pygame.font.Font:
        key = (path, size)
        if key not in cls._cache:
            cls._cache[key] = pygame.font.Font(path, size)
        return cls._cache[key]


class Icon:

    _cache: dict[str, pygame.Surface] = {}

    def __init__(self, path: str, size: int | tuple[int, int] | None = None
                 ) -> None:
        self.path = path
        self._original = self._load(path)
        if isinstance(size, int):
            size = (size, size)
        self.surface = (
            pygame.transform.smoothscale(self._original, size)
            if size else self._original
        )

    @classmethod
    def _load(cls, path: str) -> pygame.Surface:
        if path not in cls._cache:
            cls._cache[path] = pygame.image.load(path).convert_alpha()
        return cls._cache[path]

    def resized(self, size: int | tuple[int, int]) -> "Icon":
        if isinstance(size, int):
            size = (size, size)
        new_icon = Icon.__new__(Icon)
        new_icon.path = self.path
        new_icon._original = self._original
        new_icon.surface = pygame.transform.smoothscale(self._original, size)
        return new_icon

    def get_rect(self, **kwargs) -> pygame.Rect:
        return self.surface.get_rect(**kwargs)

    def draw(self, target: pygame.Surface, pos: tuple[int, int]) -> None:
        target.blit(self.surface, pos)


_SPRITESHEETS: dict[str: list[pygame.Surface]] = {}


def load_spritesheet(name: str,
                     t_width: int,
                     t_height: int,
                     ) -> list[pygame.Surface]:
    if name not in _SPRITESHEETS:
        path = os.path.join(bpath, name)
        _SPRITESHEETS[name] = load_spritesheet(path, t_width, t_height)
    return _SPRITESHEETS[name]


DRN_DEATH = partial(load_spritesheet, "drone_death.png", 120, 100)
DRN_WALK = partial(load_spritesheet, "drone_WALK.png", 120, 100)
DRN_IDLE = partial(load_spritesheet, "drone_IDLE.png", 120, 80)
DRN_SCAN = partial(load_spritesheet, "drone_scan.png", 120, 80)

BOPS_FONT = partial(Font, os.path.join(bpath, "BlackOpsOne-Regular.ttf"))
DIRT_FONT = partial(Font, os.path.join(bpath, "RubikDirt-Regular.ttf"))
FAST_FONT = partial(Font, os.path.join(bpath, "FasterOne-Regular.ttf"))

BACK_ICON = partial(Icon, os.path.join(bpath, "arrow_back.png"))
CLEAR_ICON = partial(Icon, os.path.join(bpath, "clear.png"))
CLOSE_ICON = partial(Icon, os.path.join(bpath, "close.png"))
DOWN_ICON = partial(Icon, os.path.join(bpath, "down.png"))
EASY_ICON = partial(Icon, os.path.join(bpath, "easy.png"))
HARD_ICON = partial(Icon, os.path.join(bpath, "hard.png"))
HELP_ICON = partial(Icon, os.path.join(bpath, "help.png"))
HOME_ICON = partial(Icon, os.path.join(bpath, "home.png"))
IMPOSSIBLE_ICON = partial(Icon, os.path.join(bpath, "impossible.png"))
LOUT_ICON = partial(Icon, os.path.join(bpath, "logout.png"))
MEDIUM_ICON = partial(Icon, os.path.join(bpath, "medium.png"))
MENU_ICON = partial(Icon, os.path.join(bpath, "menu.png"))
NEXT_ICON = partial(Icon, os.path.join(bpath, "next.png"))
RESET_ICON = partial(Icon, os.path.join(bpath, "reset.png"))
SETTING_ICON = partial(Icon, os.path.join(bpath, "settings.png"))
START_ICON = partial(Icon, os.path.join(bpath, "start.png"))
UP_ICON = partial(Icon, os.path.join(bpath, "up.png"))
