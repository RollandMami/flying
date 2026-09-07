# from typing import Protocol, Any
import pygame
from infrastructure import map_model as mm
from ..settings import rainbow
from .drone import Drone


class Landing:
    def __init__(self,
                 bg: pygame.Color,
                 default: pygame.Color,
                 hub: mm.Hub,
                 radius: int = 30) -> None:
        self.bb = bg
        self.cost = hub.cost
        self.name = hub.name
        self.default_color = default
        self.max_capacity = hub.max_drone
        self.description = hub.description
        self.is_priority = hub.is_priority
        self.is_crossable = hub.is_crossable
        self.pos = pygame.Vector2(hub.x, hub.y)
        self.color = self._resolve_color(hub.color)
        self.drones: list[Drone] = []

    def _resolve_color(self, col: str | None
                       ) -> pygame.Color | list[pygame.Color]:
        if not col:
            return self.default_color
        elif col == "rainbow":
            return rainbow()
        return pygame.Color(col)

    def can_land(self) -> bool:
        return len(self.drones) < self.max_capacity

    def receive(self, drn: Drone) -> None:
        self.drones.append(drn)

    def send(self, _to: "Landing") -> None:
        if not self.drones:
            raise ValueError("Lands don't have drones")
        drn = self.drones.pop()
        drn.move(_to.pos)
