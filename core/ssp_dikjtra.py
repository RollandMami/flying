from .base_mfmc import BaseMFMC
from typing import Any
from .ResidualGraph import ResidualGraph
from .Station import Station
from math import inf

class Solver(BaseMFMC):
    def costxcapaticy(self, hubs: Station) -> int:
        return hubs.cost * hubs.max_capacity

    def findPath(self,
                graph: ResidualGraph,
                start: Station,
                goal: Station,
                path=None
                ):
        parent = {}
        pile = []
        pile.append(start)
        current: Station = start
        while pile and current != goal:
            voisin = current.connected_hubs

            for v in voisin:
                if voisin[v]


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
