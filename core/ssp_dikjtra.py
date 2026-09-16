from .base_mfmc import BaseMFMC
from typing import Any
from .ResidualGraph import ResidualGraph


class Solver(BaseMFMC):
    def solve(self,
              graph: ResidualGraph
              ) -> dict[str, Any]:
        scenario = {}
        drones = graph.drones
        hubs = graph._all_hubs
        start_hub = hubs[0]
        end_hub = hubs[1]
        # initialise, mettre tout les drones dans le starthub:
        scenario["t0"] = [
            f"{drone.id}-{start_hub.name}" for drone in drones
        ]
        i = 1
        visited = []
        while not graph._finished:
            voisins = []
            ...
        return scenario
