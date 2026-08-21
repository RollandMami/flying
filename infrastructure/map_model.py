from enum import Enum
import importlib
from typing import Optional

try:
    pydantic = importlib.import_module("pydantic")
    BaseModel = pydantic.BaseModel
    Field = pydantic.Field
    ValidationError = pydantic.ValidationError
    model_validator = pydantic.model_validator
    field_validator = pydantic.field_validator
except (ModuleNotFoundError, ImportError) as e:
    raise ModuleNotFoundError(f"{type(e).__name__}: {e}")


class Zone(str, Enum):
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"

    @property
    def cost(self) -> int | None:
        return {
            Zone.NORMAL: 1,
            Zone.RESTRICTED: 2,
            Zone.PRIORITY: 1,
        }.get(self)

    @property
    def is_crossable(self) -> bool:
        return self is not Zone.BLOCKED

    @property
    def is_priority(self) -> bool:
        return self is Zone.PRIORITY


class Meta(BaseModel):
    color: str | None = Field(default=None)
    max_drones: int = Field(default=1, ge=1)
    zone: Zone = Field(default=Zone.NORMAL)

    @field_validator("color")
    @classmethod
    def validate_color(cls, v: str | None) -> str | None:
        if v is None:
            return v
        v = v.strip()
        if not v:
            return None
        if any(ch.isspace() for ch in v):
            raise ValueError(f"color must be a single word, got: '{v}'")
        return v.lower()
 
    @property
    def cost(self) -> int | None:
        return self.zone.cost
 
    @property
    def is_traversable(self) -> bool:
        return self.zone.is_crossable


class Hub(BaseModel):
    name: str
    x: float
    y: float
    meta: Meta = Field(default_factory=Meta)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Hub name must not be empty")
        if "-" in v:
            raise ValueError(f"Hub name must not contain '-': '{v}'")
        return v


class Con(BaseModel):
    left: str
    right: str
    max_link_capacity: Optional[int] = Field(default=1, ge=1)

    @model_validator(mode="after")
    def check_no_self_loop(self) -> "Con":
        if self.left == self.right:
            raise ValueError(f"Self-loop connection not allowed: '{self.left}-{self.right}'")
        return self


class MapModel(BaseModel):
    drone_number: int
    start_hub: Hub
    hubs: list[Hub] = Field(default_factory=list)
    end_hub: Hub
    connections: list[Con] = Field(default_factory=list)

    @model_validator(mode="after")
    def check_connections_reference_known_hubs(self) -> "MapModel":
        known_names = {h.name for h in self.hubs}
        known_names.add(self.start_hub.name)
        known_names.add(self.end_hub.name)

        for c in self.connections:
            if c.left not in known_names:
                raise ValueError(f"Connection ref unknown: {c.left}")
            if c.right not in known_names:
                raise ValueError(f"Connection ref unknown: {c.right}")
        return self

    @model_validator(mode="after")
    def check_unique_hub_names(self) -> "MapModel":
        names = [h.name for h in self.hubs]
        names += [self.start_hub.name, self.end_hub.name]
        dupes = {n for n in names if names.count(n) > 1}
        if dupes:
            raise ValueError(f"Duplicate hub name(s): {sorted(dupes)}")
        return self
 
    @model_validator(mode="after")
    def check_start_end_not_blocked(self) -> "MapModel":
        if not self.start_hub.meta.zone.is_crossable:
            raise ValueError(f"start_hub '{self.start_hub.name}' cannot be blocked")
        if not self.end_hub.meta.zone.is_crossable:
            raise ValueError(f"end_hub '{self.end_hub.name}' cannot be blocked")
        return self


    def get_hub(self, name: str) -> Hub:
        if self.start_hub.name == name:
            return self.start_hub
        if self.end_hub.name == name:
            return self.end_hub
        for h in self.hubs:
            if h.name == name:
                return h
        raise KeyError(name)

    def hub_cost(self, name: str) -> int | None:
        """Cout de deplacement pour entrer dans le hub `name`.
        None => zone bloquee, chemin invalide si elle est utilisee."""
        return self.get_hub(name).meta.cost
