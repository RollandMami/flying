from infrastructure import MapModel
from .Station import Station
from .AirCrossPlane import AirCrossPlane
from typing import Any


class ResidualGraph:
    def __init__(self,
                 data: MapModel,
                 viewport_center: tuple[float, float],
                 margin: int = 200,
                 speed: int = 50,
                 pan_speed: int = 300) -> None:
        self.speed = speed
        self.margin = margin
        self._dragging = False
        self.pan_speed = pan_speed
        self.map_data_model = data
        self.viewport_center = viewport_center
        self.offset_x, self.offset_y = self._compute_offset()
        self.lands = {
            hub.name: Station(hub, data.connections,
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
        AirCrossPlane.reset_ids()
        self.drones = [
            AirCrossPlane((sx, sy), l_name=self.start_land.name)
            for _ in range(self.map_data_model.nb_drones)
        ]
        for drone in self.drones:
            self.start_land.receive(drone)

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
        mcx, mcy = self.viewport_center
        bcx, bcy = self._center

        scaled_cx = bcx * self.margin
        scaled_cy = bcy * self.margin
        return mcx - scaled_cx, mcy - scaled_cy
