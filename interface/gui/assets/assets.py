import pygame
from functools import partial
from typing import Any
import os

bpath = "/".join(os.path.abspath(__file__).split("/")[:-1])


class Font:
    _cache: dict[tuple[str, int], pygame.font.Font] = {}

    @classmethod
    def get(cls, path: str, size: int) -> pygame.font.Font:
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
    def from_surface(cls, surface: pygame.Surface, path: str = "") -> "Icon":
        icon = cls.__new__(cls)
        icon.path = path
        icon._original = surface
        icon.surface = surface
        return icon

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

    def get_rect(self, **kwargs: Any) -> pygame.Rect:
        return self.surface.get_rect(**kwargs)

    def draw(self, target: pygame.Surface, pos: tuple[int, int]) -> None:
        target.blit(self.surface, pos)


_SPRITESHEETS: dict[str, list[pygame.Surface]] = {}


def splites(path: str, width: int, height: int) -> list[Icon]:
    sheet = pygame.image.load(path).convert_alpha()
    sheet_w, sheet_h = sheet.get_size()

    cols = sheet_w // width
    rows = sheet_h // height

    if cols == 0 or rows == 0:
        raise ValueError(
            f"'{path}': image de taille {sheet_w}x{sheet_h} trop petite "
            f"pour des tiles de {width}x{height} (cols={cols}, rows={rows})"
        )

    frames = []
    for row in range(rows):
        for col in range(cols):
            rect = pygame.Rect(col * width, row * height, width, height)
            frame = sheet.subsurface(rect).copy()
            frames.append(Icon.from_surface(frame, path))
    return frames


def load_spritesheet(name: str,
                     t_width: int,
                     t_height: int,
                     ) -> list[Icon]:
    if name not in _SPRITESHEETS:
        path = os.path.join(bpath, name)
        _SPRITESHEETS[name] = splites(path, t_width, t_height)
    return _SPRITESHEETS[name]


DRN_DEATH = partial(load_spritesheet, "drone_death.png", 120, 100)
DRN_WALK = partial(load_spritesheet, "drone_WALK.png", 120, 80)
DRN_IDLE = partial(load_spritesheet, "drone_IDLE.png", 120, 80)
DRN_SCAN = partial(load_spritesheet, "drone_scan.png", 120, 80)

BOPS_FONT = partial(Font.get, os.path.join(bpath, "BlackOpsOne-Regular.ttf"))
DIRT_FONT = partial(Font.get, os.path.join(bpath, "RubikDirt-Regular.ttf"))
FAST_FONT = partial(Font.get, os.path.join(bpath, "FasterOne-Regular.ttf"))

MENU_ICON = partial(Icon, os.path.join(bpath, "menu.png"))
HOME_ICON = partial(Icon, os.path.join(bpath, "home.png"))

LOGO_RLD_ICON = partial(Icon, os.path.join(bpath, "logo_rolland.png"))
LOGO_42_ICON = partial(Icon, os.path.join(bpath, "LOGO_42.png"))

BACK_ICON = partial(Icon, os.path.join(bpath, "arrow_back.png"))
NEXT_ICON = partial(Icon, os.path.join(bpath, "next.png"))

DOWN_ICON = partial(Icon, os.path.join(bpath, "down.png"))
UP_ICON = partial(Icon, os.path.join(bpath, "up.png"))
RDO_CHECK_ICON = partial(Icon, os.path.join(bpath, "rdo_checked.png"))
RDO_UNCHEK_ICON = partial(Icon, os.path.join(bpath, "rdo_unchecked.png"))

START_ICON = partial(Icon, os.path.join(bpath, "start.png"))
SETTING_ICON = partial(Icon, os.path.join(bpath, "settings.png"))
LOUT_ICON = partial(Icon, os.path.join(bpath, "logout.png"))
HELP_ICON = partial(Icon, os.path.join(bpath, "help.png"))

CLEAR_ICON = partial(Icon, os.path.join(bpath, "clear.png"))
CLOSE_ICON = partial(Icon, os.path.join(bpath, "close.png"))
RESET_ICON = partial(Icon, os.path.join(bpath, "reset.png"))
SAVE_ICON = partial(Icon, os.path.join(bpath, "save.png"))

EASY_ICON = partial(Icon, os.path.join(bpath, "easy.png"))
MEDIUM_ICON = partial(Icon, os.path.join(bpath, "medium.png"))
HARD_ICON = partial(Icon, os.path.join(bpath, "hard.png"))
IMPOSSIBLE_ICON = partial(Icon, os.path.join(bpath, "impossible.png"))
