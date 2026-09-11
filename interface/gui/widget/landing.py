import pygame
from infrastructure import map_model as mm
from ..settings import rainbow
from .drone import Drone
from .components import Label
from core.Station import Station
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
        self.logic = Station(hub, link, offset, margin)
        self.bg = bg
        self.fg = fg
        self.r = radius
        self.font = font
        self.master = master
        self.default_color = default
        self.color: list[pygame.Color] = self._resolve_color(hub.color)
        self.rect = pygame.Rect(self.x - self.r,
                                self.y - self.r,
                                2 * self.r, 2 * self.r)
        x, y = self.pos
        base_lbl = partial(Label, font=font, bg_color=bg,
                           font_color=fg, master=master, anchor="center")
        self.l_name = base_lbl(self.name.upper(), position=(x, y - 70))
        self.l_description = base_lbl(self.description, position=(x, y - 55))
        self.l_capacitor = base_lbl(
            self.logic._capacity_text(), position=(x, y - 40))

    @property
    def x(self) -> float:
        return self.logic.x

    @property
    def y(self) -> float:
        return self.logic.y

    @property
    def pos(self) -> tuple[float, float]:
        return self.logic.pos

    @property
    def name(self) -> str:
        return self.logic.name

    @property
    def description(self) -> str:
        return self.logic.description

    @property
    def max_capacity(self) -> int:
        return self.logic.max_capacity

    @property
    def drones(self):
        return self.logic.drones

    @property
    def connected_hubs(self) -> dict[str, int]:
        return self.logic.connected_hubs

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

    def _resolve_color(self, col: str | None
                       ) -> list[pygame.Color]:
        if not col:
            return [pygame.Color(self.default_color)]
        elif col == "rainbow":
            return [pygame.Color(*rgb) for rgb in rainbow()]
        return [pygame.Color(col)]

    def receive(self, drn: Drone) -> bool:
        if not self.logic.receive(drn):
            return False
        self.l_capacitor.set_text(self.logic._capacity_text())
        return True

    def send(self, _to: "Landing", nb: int = 1) -> None:
        self.logic.send(_to.logic, nb)
        self.l_capacitor.set_text(self.logic._capacity_text())
        _to.l_capacitor.set_text(_to.logic._capacity_text())

    def pan(self, dx: float, dy: float) -> None:
        self.logic.pan(dx, dy)
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
