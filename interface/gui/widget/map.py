import pygame
from infrastructure import MapModel
from .landing import Landing
from .components import Grid
from typing import Any


class MapManager:
    def __init__(self,
                 font: pygame.font.Font,
                 bg: pygame.Color,
                 fg: pygame.Color,
                 master: pygame.Surface,
                 data: MapModel,
                 margin: int = 160):
        self.bg = bg
        self.fg = fg
        self.font = font
        self.master = master
        self.margin = margin
        self.map_data_model = data
        self.offset_x, self.offset_y = self._compute_offset()
        self.grid = Grid(None, self.bg, self.fg,
                         self.master, (margin, margin), 40)
        self.lands = [
            Landing(self.font, self.bg, self.fg,
                    self.master, "red", land, 30,
                    offset=(self.offset_x, self.offset_y),
                    margin=self.margin)
            for land in self._all_hubs
            ]

    def event_handler(self, event: pygame.event.Event) -> None:
        pass

    def update(self, dt: float) -> None:
        pass

    def draw(self) -> None:
        self.grid.draw()
        for land in self.lands:
            land.draw()

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
    def _center(self) -> tuple[int, int]:
        minx, maxx, miny, maxy = self._bounds
        return (maxx - minx) // 2, (maxy - miny) // 2

    def _compute_offset(self) -> None:
        mcx, mcy = self.master.get_rect().center
        bcx, bcy = self._center

        scaled_cx = bcx * self.margin
        scaled_cy = bcy * self.margin
        return mcx - scaled_cx, mcy - scaled_cy
