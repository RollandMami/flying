import pygame
from ..assets import assets
import itertools


class Drone:
    def __init__(self,
                 width: int,
                 height: int,
                 bg: pygame.Color,
                 position: tuple[int, int],
                 master: pygame.Surface) -> None:
        self.position = position
        self.bg = bg
        self.master = master
        self.width = width
        self.height = height
        self.walk_img = assets.DRN_WALK()
        self.death_img = assets.DRN_DEATH()
        self.idle_img = assets.DRN_IDLE()
        self.scan_img = assets.DRN_SCAN()

        self.idle_cycle = itertools.cycle(self.idle_img)
        self.walk_cycle = itertools.cycle(self.walk_img)
        self.death_cycle = itertools.cycle(self.death_img)
        self.scan_cycle = itertools.cycle(self.scan_img)

        self.rect = pygame.Rect((self.position), (self.width, self.height))
        self.actual_img = self.idle_img[0]
        self.actual_img_rect = self.actual_img.get_rect(
            center=self.rect.center
        )

        self.animation = {
            "WALK": lambda: self.walk(0),
            "IDLE": lambda: self.idle(0),
            "SCAN": lambda: self.scan(0),
            "DEATH": lambda: self.death(0)
        }

        self.frame_duration = 0.1
        self.anim_timer = 0.0

    def draw(self) -> None:
        pygame.draw.rect(self.master, self.bg, self.rect)
        self.master.blit(self.actual_img, self.actual_img_rect)

    def set_position(self, x: float, y: float) -> None:
        self.rect.x, self.rect.y = x, y
        self.actual_img_rect = self.actual_img.get_rect(
            center=self.rect.center
        )

    def move(self, speed: float, new_pos: tuple[int, int]) -> None:
        x, y = self.position
        new_x, new_y = x + speed, y + speed
        if new_x <= new_pos[0]:
            self.position = (new_x, y)
            self.set_position(new_x, y)
        if new_y <= new_pos[0]:
            self.set_position(self.position[0], new_y)

    def idle(self, dt: float) -> None:
        self.anim_timer += dt
        if self.anim_timer >= self.frame_duration:
            self.anim_timer -= self.frame_duration
            self.actual_img = next(self.idle_cycle)
            self.actual_img_rect = self.actual_img.get_rect(
                center=self.actual_img_rect.center
            )

    def update(self, dt: int) -> None:
        self.walk(dt)

    def event_handler(self, event: pygame.event.Event) -> None:
        ...

    def walk(self, dt: float) -> None:
        self.anim_timer += dt
        if self.anim_timer >= self.frame_duration:
            self.anim_timer -= self.frame_duration
            self.actual_img = next(self.walk_cycle)
            self.actual_img_rect = self.actual_img.get_rect(
                center=self.actual_img_rect.center
            )

    def scan(self, dt: float) -> None:
        ...

    def death(self, dt: float) -> None:
        ...
