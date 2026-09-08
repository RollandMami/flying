# from typing import Protocol, Any
import pygame
from infrastructure import map_model as mm
from ..settings import rainbow
from .drone import Drone
from .components import Label
from functools import partial


class Landing:
    def __init__(self,
                 font: pygame.font.Font,
                 bg: pygame.Color,
                 fg: pygame.Color,
                 master: pygame.Surface,
                 default: pygame.Color,
                 hub: mm.Hub,
                 radius: int = 30,
                 offset: tuple[int, int] = (0, 0),
                 margin: int = 1) -> None:
        ox, oy = offset
        self.bb = bg
        self.x = hub.x * margin + ox
        self.y = hub.y * margin + oy
        self.r = radius
        self.master = master
        self.cost = hub.cost
        self.name = hub.name.upper()
        self.default_color = default
        self.max_capacity = hub.max_drone
        self.description = hub.description
        self.is_priority = hub.is_priority
        self.is_crossable = hub.is_crossable
        self.pos = pygame.Vector2(self.x, self.y)
        self.color = self._resolve_color(hub.color)
        self.drones: list[Drone] = []
        self.rect = pygame.Rect(self.x - self.r,
                                self.y - self.r,
                                2 * self.r, 2 * self.r)
        x, y = self.pos
        base_lbl = partial(Label, font=font, bg_color=bg,
                           font_color=fg, master=master, anchor="center")
        self.l_name = base_lbl(self.name, position=(x, y - 70))
        self.l_description = base_lbl(self.description, position=(x, y - 55))
        self.l_capacitor = base_lbl(
            self._capacity_text(), position=(x, y - 40))

    def _capacity_text(self) -> str:
        return f"DRN: {len(self.drones):02d}/{self.max_capacity:02d}"

    def _resolve_color(self, col: str | None
                       ) -> pygame.Color:  # | list[pygame.Color]:
        if not col:
            return self.default_color
        elif col == "rainbow":
            return rainbow()[0]
        return pygame.Color(col)

    def can_land(self) -> bool:
        return len(self.drones) < self.max_capacity

    def receive(self, drn: Drone) -> None:
        if self.can_land():
            self.drones.append(drn)
            self.l_capacitor.set_text(self._capacity_text())

    def send(self, _to: "Landing") -> None:
        if not self.drones:
            raise ValueError("Lands don't have drones")
        drn = self.drones.pop()
        drn.move(_to.pos)
        self.l_capacitor.set_text(self._capacity_text())

    def draw(self) -> None:
        pygame.draw.circle(self.master, self.color, self.rect.center, self.r)
        self.l_name.draw()
        self.l_description.draw()
        self.l_capacitor.draw()
