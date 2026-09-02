import pygame
from ..assets import assets
import itertools
from typing import Protocol


class Icons(Protocol):
    def resized(self, size: int | tuple[int, int]) -> "Icons":
        ...

    def draw(self, target: pygame.Surface, pos: tuple[int, int]) -> None:
        ...


class Drone:

    class Animate:

        _resize_cache: dict[
            tuple[int, int | tuple[int, int]], list[Icons]] = {}

        def __init__(self, master_rect: pygame.Rect,
                     size: int | tuple[int, int]) -> None:
            self.w = master_rect.width
            self.death_img = self._sized(assets.DRN_DEATH(), size)
            self.walk_img = self._sized(assets.DRN_WALK(), size)
            self.idle_img = self._sized(assets.DRN_IDLE(), size)
            self.scan_img = self._sized(assets.DRN_SCAN(), size)

            self.idle_cycle = itertools.cycle(self.idle_img)
            self.walk_cycle = itertools.cycle(self.walk_img)
            self.death_cycle = itertools.cycle(self.death_img)
            self.scan_cycle = itertools.cycle(self.scan_img)

            self.frame_duration = 0.1
            self.anim_timer = 0.0
            self.actual_img = self.idle_img[0]
            self.actual_img_rect = self.actual_img.get_rect(
                center=master_rect.center
            )

        @classmethod
        def _sized(cls, icons: list[Icons], size) -> list:
            if not size:
                return icons
            key = (id(icons), size)
            if key not in cls._resize_cache:
                cls._resize_cache[key] = [icon.resized(size) for icon in icons]
            return cls._resize_cache[key]

        def iter_image(self, dt: float, cycle: itertools.cycle) -> None:
            self.anim_timer += dt
            if self.anim_timer >= self.frame_duration:
                self.anim_timer -= self.frame_duration
                self.actual_img = next(cycle)
                self.actual_img_rect = self.actual_img.get_rect(
                    center=self.actual_img_rect.center
                )

        def idle(self, dt: float) -> None:
            self.iter_image(dt, self.idle_cycle)

        def walk(self, dt: float) -> None:
            self.iter_image(dt, self.walk_cycle)

        def scan(self, dt: float) -> None:
            self.iter_image(dt, self.scan_cycle)

        def death(self, dt: float) -> None:
            self.iter_image(dt, self.death_cycle)

    def __init__(self,
                 width: int,
                 height: int,
                 bg: pygame.Color,
                 position: tuple[int, int],
                 master: pygame.Surface,
                 sprite_size: int | tuple[int, int] | None = None
                 ) -> None:
        self.position = position
        self.bg = bg
        self.master = master
        self.width = width
        self.height = height
        self.target_pos = None

        self.rect = pygame.Rect((self.position), (self.width, self.height))
        self.anim = self.Animate(self.rect, sprite_size)

    def draw(self) -> None:
        pygame.draw.rect(self.master, self.bg, self.rect)
        self.anim.actual_img.draw(
            self.master,
            self.anim.actual_img_rect.topleft)

    def set_position(self, x: float, y: float) -> None:
        self.rect.x, self.rect.y = x, y
        self.anim.actual_img_rect = self.anim.actual_img.get_rect(
            center=self.rect.center
        )

    def move(self, new_pos: tuple[int, int]) -> None:
        self.target_pos = new_pos

    def update(self, dt: int, speed: float) -> None:
        self.anim.idle(dt)
        if self.target_pos is None:
            return
        x, y = self.position
        target_x, target_y = self.target_pos
        dx = target_x - x
        dy = target_y - y
        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance == 0:
            self.target_pos = None
            return

        movement = speed * dt

        if distance <= movement:
            x = target_x
            y = target_y
        else:
            x += dx / distance * movement
            y += dy / distance * movement

        self.position = (x, y)
        self.set_position(x, y)

        if self.position == self.target_pos:
            self.target_pos = None

    def event_handler(self, event: pygame.event.Event) -> None:
        pass
