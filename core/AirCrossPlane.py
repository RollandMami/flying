
class AirCrossPlane:
    _next_id = 1

    def __init__(self,
                 position: tuple[int, int],
                 l_name: str = "Zone Neutre") -> None:
        self.position = position
        self.land_name = l_name
        self.target_pos = None
        self.id = AirCrossPlane._next_id
        AirCrossPlane._next_id += 1

    @classmethod
    def reset_ids(cls) -> None:
        cls._next_id = 1

    def move(self, new_pos: tuple[int, int]) -> None:
        self.target_pos = new_pos

    def update(self, dt: float, speed: float) -> bool:
        if self.target_pos is None:
            return False

        x, y = self.position
        target_x, target_y = self.target_pos
        dx, dy = target_x - x, target_y - y
        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance == 0:
            self.target_pos = None
            return False

        movement = speed * dt
        if distance <= movement:
            x, y = target_x, target_y
        else:
            x += dx / distance * movement
            y += dy / distance * movement

        self.position = (x, y)
        if self.position == self.target_pos:
            self.target_pos = None
        return True

    def pan(self, dx: float, dy: float) -> None:
        x, y = self.position
        self.position = (x + dx, y + dy)
        if self.target_pos is not None:
            tx, ty = self.target_pos
            self.target_pos = (tx + dx, ty + dy)
