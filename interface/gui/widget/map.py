import pygame
from infrastructure import MapModel
from .landing import Landing
from .components import Grid, Label
from typing import Any
from .drone import Drone


class MapManager:
    def __init__(self,
                 font: pygame.font.Font,
                 bg: pygame.Color,
                 fg: pygame.Color,
                 master: pygame.Surface,
                 data: MapModel,
                 margin: int = 200):
        self.bg = bg
        self.fg = fg
        self.font = font
        self.master = master
        self.margin = margin
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
                              margin=self.margin, )
            for hub in self._all_hubs
            }
        start = self.map_data_model.start_hub
        sx = start.x * self.margin + self.offset_x
        sy = start.y * self.margin + self.offset_y
        Drone.reset_ids()
        self.drones = [
            Drone(40, 40, self.bg, (sx, sy), self.master, 40, show_id=True)
            for _ in range(self.map_data_model.nb_drones)
        ]
        for drone in self.drones:
            self.lands["start"].receive(drone)

    def event_handler(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.lands["start"].send(self.lands["waypoint1"])

    def update(self, dt: float) -> None:
        for drone in self.drones:
            drone.update(dt, speed=50)

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
                             land_b.pos, 14)
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
        xs = [hub.x for hub in self._all_hubs]
        ys = [hub.y for hub in self._all_hubs]
        return min(xs), max(xs), min(ys), max(ys)

    @property
    def _center(self) -> tuple[float, float]:
        minx, maxx, miny, maxy = self._bounds
        return (maxx + minx) / 2, (maxy + miny) / 2

    def _compute_offset(self) -> None:
        mcx, mcy = self.master.get_rect().center
        bcx, bcy = self._center

        scaled_cx = bcx * self.margin
        scaled_cy = bcy * self.margin
        return mcx - scaled_cx, mcy - scaled_cy
