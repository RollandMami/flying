import pygame
from ..assets import assets
import itertools
from typing import Protocol
from .components import Label


class Icons(Protocol):
    def resized(self, size: int | tuple[int, int]) -> "Icons":
        ...

    def draw(self, target: pygame.Surface, pos: tuple[int, int]) -> None:
        ...


class Drone:
    _next_id = 0

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
                 sprite_size: int | tuple[int, int] | None = None,
                 l_name: str = "Zone Neutre",
                 show_id: bool = False) -> None:
        self.position = position
        self.bg = bg
        self.font = assets.BOPS_FONT(10)
        self.land_name = l_name
        self.master = master
        self.width = width
        self.height = height
        self.target_pos = None
        self._id = Drone._next_id
        Drone._next_id += 1
        self.show_id = show_id

        self.rect = pygame.Rect((0, 0), (self.width, self.height))
        self.rect.center = self.position
        self.anim = self.Animate(self.rect, sprite_size)
        self.id_lbl = Label(f"{self._id:02d}", self.font,
                            self.bg, "white", self.master, self.position,
                            anchor="center")

    def draw(self) -> None:
        # pygame.draw.rect(self.master, self.bg, self.rect)
        self.anim.actual_img.draw(
            self.master,
            self.anim.actual_img_rect.topleft)
        if self.show_id:
            self.id_lbl.draw()

    def set_position(self, x: float, y: float) -> None:
        self.rect.center = (x, y)
        self.anim.actual_img_rect = self.anim.actual_img.get_rect(
            center=self.rect.center
        )

    def move(self, new_pos: tuple[int, int]) -> None:
        self.target_pos = new_pos

    def set_anim(self, dt: float, anim: str | None) -> None:
        if not anim or anim == "idle":
            self.anim.idle(dt)
        elif anim == "walk":
            self.anim.walk(dt)
        elif anim == "scan":
            self.anim.scan(dt)
        elif anim == "death":
            self.anim.death(dt)

    def update(self, dt: int, speed: float) -> None:
        if self.target_pos is None:
            self.set_anim(dt, "idle")
            return

        x, y = self.position
        target_x, target_y = self.target_pos
        dx = target_x - x
        dy = target_y - y
        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance == 0:
            self.target_pos = None
            self.set_anim(dt, "idle")
            return

        self.set_anim(dt, "walk")
        movement = speed * dt

        if distance <= movement:
            x = target_x
            y = target_y
        else:
            x += dx / distance * movement
            y += dy / distance * movement

        self.position = (x, y)
        self.set_position(x, y)
        self.id_lbl.set_pos((x, y))

        if self.position == self.target_pos:
            self.target_pos = None

    def event_handler(self, event: pygame.event.Event) -> None:
        pass
