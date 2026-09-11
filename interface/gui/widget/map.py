import pygame
from infrastructure import MapModel
from .landing import Landing
from .components import Grid, Label
from typing import Any
from .drone import Drone
from core.ResidualGraph import ResidualGraph


class MapManager:
    def __init__(self,
                 font: pygame.font.Font,
                 bg: pygame.Color,
                 fg: pygame.Color,
                 master: pygame.Surface,
                 data: MapModel,
                 margin: int = 200,
                 speed: int = 50,
                 pan_speed: int = 300) -> None:
        self.bg = bg
        self.fg = fg
        self.font = font
        self.speed = speed
        self.master = master
        self.graph = ResidualGraph(
            data,
            viewport_center=master.get_rect().center,
            margin=margin,
            speed=speed,
            pan_speed=pan_speed
        )
        self.margin = margin
        self._dragging = False
        self.pan_speed = pan_speed
        self.map_data_model = data
        self.offset_x, self.offset_y = self._compute_offset()
        self.grid = Grid(None, self.bg, self.fg,
                         self.master, (margin, margin), 40,
                         origin=(
                             int(self.offset_x),
                             int(self.offset_y)))
        self.lands = {
            hub.name: Landing(self.font, self.bg, self.fg,
                              self.master, "red", hub,
                              data.connections, 30,
                              offset=(self.offset_x, self.offset_y),
                              margin=self.margin)
            for hub in self._all_hubs
            }
        start = self.map_data_model.start_hub
        end = self.map_data_model.end_hub

        self.start_land = self.lands[start.name]
        self.end_land = self.lands[end.name]
        sx = start.x * self.margin + self.offset_x
        sy = start.y * self.margin + self.offset_y
        Drone.reset_ids()
        self.drones = [
            Drone(40, 40, self.bg, (sx, sy), self.master, 40, show_id=True)
            for _ in range(self.map_data_model.nb_drones)
        ]
        for drone in self.drones:
            self.start_land.receive(drone)

    def event_handler(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._dragging = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self._dragging = False
        elif event.type == pygame.MOUSEMOTION and self._dragging:
            dx, dy = event.rel
            self.pan(dx, dy)

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        dx = dy = 0.0
        if keys[pygame.K_LEFT]:
            dx += self.pan_speed * dt
        if keys[pygame.K_RIGHT]:
            dx -= self.pan_speed * dt
        if keys[pygame.K_UP]:
            dy += self.pan_speed * dt
        if keys[pygame.K_DOWN]:
            dy -= self.pan_speed * dt
        if dx or dy:
            self.pan(dx, dy)

        for drone in self.drones:
            drone.update(dt, self.speed)

    def draw(self) -> None:
        self.draw_connection()
        self.grid.draw()
        for land in self.lands.values():
            land.draw()
        for drone in self.drones:
            drone.draw()

    def draw_connection(self) -> None:
        drawn = set()
        for con in self.map_data_model.connections:
            pair = frozenset((con.left, con.right))
            if pair in drawn:
                continue
            drawn.add(pair)
            land_a = self.lands[con.left]
            land_b = self.lands[con.right]
            pygame.draw.line(self.master, "magenta", land_a.pos,
                             land_b.pos, 8)
            mid = self._mid_point(land_a.pos, land_b.pos)
            Label(f"{con.max_link_capacity:02d}", self.font, "white",
                  "black", self.master, mid, anchor="center").draw()

    @staticmethod
    def _mid_point(a: tuple[float, float], b: tuple[float, float]
                   ) -> tuple[float, float]:
        return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)

    @property
    def _all_hubs(self) -> list[Any]:
        return [
            self.map_data_model.start_hub,
            self.map_data_model.end_hub,
            *self.map_data_model.hubs
        ]

    @property
    def _bounds(self) -> tuple[int, int, int, int]:
        hubs = self._all_hubs
        if not hubs:
            raise ValueError("Not any Hub detected")
        xs = [hub.x for hub in hubs]
        ys = [hub.y for hub in hubs]
        return min(xs), max(xs), min(ys), max(ys)

    @property
    def _center(self) -> tuple[float, float]:
        minx, maxx, miny, maxy = self._bounds
        return (maxx + minx) / 2, (maxy + miny) / 2

    def _compute_offset(self) -> tuple[float, float]:
        mcx, mcy = self.master.get_rect().center
        bcx, bcy = self._center

        scaled_cx = bcx * self.margin
        scaled_cy = bcy * self.margin
        return mcx - scaled_cx, mcy - scaled_cy

    def pan(self, dx: float, dy: float) -> None:
        self.offset_x += dx
        self.offset_y += dy
        for land in self.lands.values():
            land.pan(dx, dy)
        for drone in self.drones:
            drone.pan(dx, dy)
        self.grid.set_origin(int(self.offset_x), int(self.offset_y))
