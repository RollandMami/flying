from collections import deque
from infrastructure import map_model as mm
from .AirCrossPlane import AirCrossPlane


class Station:
    def __init__(self,
                 hub: mm.Hub,
                 link: list[mm.Con],
                 offset: tuple[int, int] = (0, 0),
                 margin: int = 1,
                 ) -> None:
        ox, oy = offset
        self.x = hub.x * margin + ox
        self.y = hub.y * margin + oy

        self.cost = hub.cost
        self.name = hub.name
        self.max_capacity = hub.max_drone
        self.description = hub.description
        self.is_priority = hub.is_priority
        self.is_crossable = hub.is_crossable

        self.drones: deque[AirCrossPlane] = deque()
        self.connected_hubs: dict[str, int] = {}
        self._fill_connection(link)

    @property
    def pos(self) -> tuple[float, float]:
        return (self.x, self.y)

    def _fill_connection(self, link: list[mm.Con]) -> None:
        for con in link:
            if self.name == con.left:
                self.connected_hubs[con.right] = con.max_link_capacity
            elif self.name == con.right:
                self.connected_hubs[con.left] = con.max_link_capacity

    def _capacity_text(self) -> str:
        return f"DRN: {len(self.drones):02d}/{self.max_capacity:02d}"

    def _is_connected_to(self, _to: "Station") -> bool:
        return _to.name in self.connected_hubs

    def can_land(self, nb: int = 1) -> bool:
        return len(self.drones) + nb <= self.max_capacity

    def receive(self, drn: AirCrossPlane) -> bool:
        if not self.can_land():
            return False
        self.drones.append(drn)
        return True

    def send(self, _to: "Station", nb: int = 1) -> None:
        if len(self.drones) < nb:
            raise ValueError("Not enough drones to send")
        if not self._is_connected_to(_to):
            print(_to.name, "ar not connected")
            return
        if nb > self.connected_hubs[_to.name]:
            print("capacity link over flow")
            return
        if not _to.can_land(nb):
            print(_to.name, "can't land any more drones")
            return
        for _ in range(nb):
            drn = self.drones.popleft()
            if _to.receive(drn):
                drn.move(_to.pos)
            else:
                self.drones.appendleft(drn)
                break

    def pan(self, dx: float, dy: float) -> None:
        self.x += dx
        self.y += dy
