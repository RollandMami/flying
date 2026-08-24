import pygame


def load_spritesheet(path: str,
					 t_width: int,
					 t_height: int,
					 ) -> list[pygame.Surface]:
	spritesheet = pygame.image.loat(path).convert_alpha()
	sheet_width, sheet_height = spritesheet.get_size()
	tiles: list[pygame.Surface] = []

	for col in range(0, sheet_width, t_width):
		s = pygame.Rect((col, 0),(t_width, t_height))
		tiles.append(s)
	return tiles



DRONE_DEATH = load_spritesheet("./drone_death.png", 120, 100)
DRONE_WALK = load_spritesheet("./drone_WALK.png", 120, 100)
DRONE_IDLE = load_spritesheet("./drone_IDLE.png", 120, 80)
DRONE_SCAN = load_spritesheet("./drone_scan.png", 120, 80)

