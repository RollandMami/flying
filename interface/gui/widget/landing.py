# from typing import Protocol, Any
from collections import deque

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
                 link: list[mm.Con],
                 radius: int = 30,
                 offset: tuple[int, int] = (0, 0),
                 margin: int = 1,
                 ) -> None:
        ox, oy = offset
        self.bg = bg
        self.fg = fg
        self.x = hub.x * margin + ox
        self.y = hub.y * margin + oy
        self.r = radius
        self.font = font
        self.master = master
        self.cost = hub.cost
        self.name = hub.name
        self.default_color = default
        self.max_capacity = hub.max_drone
        self.description = hub.description
        self.is_priority = hub.is_priority
        self.is_crossable = hub.is_crossable
        self.pos = pygame.Vector2(self.x, self.y)
        self.color: list[pygame.Color] = self._resolve_color(hub.color)
        self.drones: deque[Drone] = deque()
        self.rect = pygame.Rect(self.x - self.r,
                                self.y - self.r,
                                2 * self.r, 2 * self.r)
        x, y = self.pos
        base_lbl = partial(Label, font=font, bg_color=bg,
                           font_color=fg, master=master, anchor="center")
        self.l_name = base_lbl(self.name.upper(), position=(x, y - 70))
        self.l_description = base_lbl(self.description, position=(x, y - 55))
        self.l_capacitor = base_lbl(
            self._capacity_text(), position=(x, y - 40))
        self.connected_hubs: dict[str, int] = {}
        self._fill_connection(link)

    def _fill_connection(self, link: list[mm.Con]) -> None:
        for con in link:
            if self.name == con.left:
                self.connected_hubs[con.right] = con.max_link_capacity
            elif self.name == con.right:
                self.connected_hubs[con.left] = con.max_link_capacity

    def draw_rainbow_rings(self, surface: pygame.Surface,
                           center: tuple[float, float], max_radius: float,
                           colors: list[pygame.Color]) -> None:
        n = len(colors)
        step = max_radius / n
        for i, color in enumerate(colors):
            radius = max_radius - i * step
            pygame.draw.circle(surface, color, center, int(radius))

    def draw(self) -> None:
        self.draw_rainbow_rings(self.master, self.rect.center, self.r,
                                self.color)
        self.l_name.draw()
        self.l_description.draw()
        self.l_capacitor.draw()

    def _capacity_text(self) -> str:
        return f"DRN: {len(self.drones):02d}/{self.max_capacity:02d}"

    def _resolve_color(self, col: str | None
                       ) -> list[pygame.Color]:
        if not col:
            return [pygame.Color(self.default_color)]
        elif col == "rainbow":
            return [pygame.Color(*rgb) for rgb in rainbow()]
        return [pygame.Color(col)]

    def _is_connected_to(self, _to: "Landing") -> bool:
        return _to.name in self.connected_hubs

    def can_land(self) -> bool:
        return len(self.drones) < self.max_capacity

    def receive(self, drn: Drone) -> None:
        if self.can_land():
            self.drones.append(drn)
            self.l_capacitor.set_text(self._capacity_text())

    def send(self, _to: "Landing") -> None:
        if not self.drones:
            raise ValueError("Lands don't have drones")
        if _to.can_land():
            drn = self.drones.popleft()
            _to.receive(drn)
            drn.move(_to.pos)
            self.l_capacitor.set_text(self._capacity_text())
        else:
            print(_to.name, "cant land any more drone")

    def pan(self, dx: float, dy: float) -> None:
        self.x += dx
        self.y += dy
        self.pos = pygame.Vector2(self.x, self.y)
        self.rect.center = (self.x, self.y)
        self.l_name.set_pos((
            self.l_name.position[0] + dx,
            self.l_name.position[1] + dy
        ))
        self.l_description.set_pos((
            self.l_description.position[0] + dx,
            self.l_description.position[1] + dy
        ))
        self.l_capacitor.set_pos((
            self.l_capacitor.position[0] + dx,
            self.l_capacitor.position[1] + dy
        ))
