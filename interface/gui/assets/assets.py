import pygame


class Font:
    _cache: dict[tuple[str, int], pygame.font.Font] = {}

    def __new__(cls, path: str, size: int) -> pygame.font.Font:
        key = (path, size)
        if key not in cls._cache:
            cls._cache[key] = pygame.font.Font(path, size)
        return cls._cache[key]


class Icon:

    _cache: dict[str, pygame.Surface] = {}

    def __init__(self, path: str, size: tuple[int, int] | None = None) -> None:
        self.path = path
        self._original = self._load(path)
        self.surface = (
            pygame.transform.smoothscale(self._original, size)
            if size else self._original
        )

    @classmethod
    def _load(cls, path: str) -> pygame.Surface:
        if path not in cls._cache:
            cls._cache[path] = pygame.image.load(path).convert_alpha()
        return cls._cache[path]

    def resized(self, size: tuple[int, int]) -> "Icon":
        new_icon = Icon.__new__(Icon)
        new_icon.path = self.path
        new_icon._original = self._original
        new_icon.surface = pygame.transform.smoothscale(self._original, size)
        return new_icon

    def get_rect(self, **kwargs) -> pygame.Rect:
        return self.surface.get_rect(**kwargs)

    def draw(self, target: pygame.Surface, pos: tuple[int, int]) -> None:
        target.blit(self.surface, pos)


def load_spritesheet(path: str,
                     t_width: int,
                     t_height: int,
                     ) -> list[pygame.Surface]:
    spritesheet = pygame.image.load(path).convert_alpha()
    sheet_width, _ = spritesheet.get_size()
    tiles: list[pygame.Surface] = []

    for col in range(0, sheet_width, t_width):
        s = pygame.Rect((col, 0), (t_width, t_height))
        tiles.append(spritesheet.subsurface(s))
    return tiles


DRONE_DEATH = load_spritesheet("./drone_death.png", 120, 100)
DRONE_WALK = load_spritesheet("./drone_WALK.png", 120, 100)
DRONE_IDLE = load_spritesheet("./drone_IDLE.png", 120, 80)
DRONE_SCAN = load_spritesheet("./drone_scan.png", 120, 80)
