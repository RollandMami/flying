from typing import Any
from abc import ABC, abstractmethod


class BaseMFMC(ABC):
    @abstractmethod
    def solve(self) -> list[Any]:
        ...
