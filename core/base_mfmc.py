from typing import Any
from abc import ABC, abstractmethod
from .ResidualGraph import ResidualGraph


class BaseMFMC(ABC):
    @abstractmethod
    def solve(self, graph: ResidualGraph) -> dict[str, Any]:
        ...
