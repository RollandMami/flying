import pygame
from ..assets import assets
import itertools
from typing import Protocol
from .components import Label
from core.AirCrossPlane import AirCrossPlane


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
                 sprite_size: int | tuple[int, int] | None = None,
                 l_name: str = "Zone Neutre",
                 show_id: bool = False) -> None:
        self.logic = AirCrossPlane(position, l_name)
        self.bg = bg
        self.font = assets.BOPS_FONT(10)
        self.master = master
        self.width = width
        self.height = height
        self.show_id = show_id

        self.rect = pygame.Rect((0, 0), (self.width, self.height))
        self.rect.center = self.logic.position
        self.anim = self.Animate(self.rect, sprite_size)
        self.id_lbl = Label(f"D{self.logic.id:02d}", self.font,
                            self.bg, "white", self.master,
                            self._label_pos(*self.logic.position),
                            anchor="center")

    def draw(self) -> None:
        self.anim.actual_img.draw(
            self.master,
            self.anim.actual_img_rect.topleft)
        if self.show_id:
            self.id_lbl.draw()

    def _label_pos(self, x: float, y: float) -> tuple[float, float]:
        return (x, y - self.height // 2)

    def _sync_position(self) -> None:
        x, y = self.logic.position
        self.rect.center = (x, y)
        self.anim.actual_img_rect = self.anim.actual_img.get_rect(
            center=self.rect.center
        )
        self.id_lbl.set_pos(self._label_pos(x, y))

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
        moved = self.logic.update(dt, speed)
        self.set_anim(dt, "walk" if moved else "idle")
        if moved:
            self._sync_position()

    def move(self, new_pos: tuple[int, int]) -> None:
        self.logic.move(new_pos)

    def pan(self, dx: float, dy: float) -> None:
        self.logic.pan(dx, dy)
        self._sync_position()

    @classmethod
    def reset_ids(cls) -> None:
        AirCrossPlane.reset_ids()

    @property
    def position(self) -> tuple[int, int]:
        return self.logic.position

    @property
    def land_name(self) -> str:
        return self.logic.land_name
