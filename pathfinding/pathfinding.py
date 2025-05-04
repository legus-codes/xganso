from typing import Dict, List

from model.hex_coordinate import HexCoordinate
from model.hex_map import HexCell, HexMap


class PathfindingHelper:

    @staticmethod
    def neighbors(hex_map: HexMap, coordinate: HexCoordinate) -> List[HexCell]:
        return [hex_map[neighbor] for neighbor in coordinate.neighbors if neighbor in hex_map]

    @staticmethod
    def in_range(hex_map: HexMap, coordinate: HexCoordinate, radius: int) -> List[HexCell]:
        results = []
        for q in range(-radius, radius+1):
            for r in range(max(-radius, -radius-q), min(radius, -q+radius)+1):
                range_coordinate = coordinate + HexCoordinate(q, r)
                if range_coordinate in hex_map:
                    results.append(hex_map[range_coordinate])
        return results

    @staticmethod
    def ring(hex_map: HexMap, coordinate: HexCoordinate, distance: int) -> List[HexCell]:
        results = []
        if distance == 0:
            return [hex_map[coordinate]]
 
        directions = coordinate.directions()
        ring_coordinate = coordinate + directions[4] * distance
        for index in range(len(directions)):
            for _ in range(distance):
                if ring_coordinate in hex_map:
                    results.append(hex_map[ring_coordinate])
                ring_coordinate = ring_coordinate + directions[index]
        return results

    @staticmethod
    def bfs(hex_map: HexMap, origin: HexCoordinate, distance: int) -> List[HexCell]:
        open_set = [(origin, 0)]
        visited = {origin: 0}

        while open_set:
            current, cost = open_set.pop(0)

            for neighbor in PathfindingHelper.neighbors(hex_map, current):
                if not neighbor.is_traversable:
                    continue
                new_cost = cost + neighbor.terrain.move_cost
                n_coordinate = neighbor.coordinate
                if new_cost <= distance and (n_coordinate not in visited or new_cost < visited[n_coordinate]):
                    visited[n_coordinate] = new_cost
                    open_set.append((n_coordinate, new_cost))
        return [hex_map[coordinate] for coordinate in visited.keys()]

    @staticmethod
    def astar(hex_map: HexMap, origin: HexCoordinate, destination: HexCoordinate) -> List[HexCell]:
        open_set = [origin]
        came_from = {}
        g_score = {origin: 0}
        f_score = {origin: origin.distance(destination)}

        while open_set:
            open_set.sort(key=lambda x: f_score.get(x, 10000))
            current = open_set.pop(0)

            if current == destination:
                return PathfindingHelper._reconstruct_path(hex_map, came_from, current)
            
            for neighbor in PathfindingHelper.neighbors(hex_map, current):
                if not neighbor.is_traversable:
                    continue
                tentative_g_score = g_score.get(current, 10000) + neighbor.terrain.move_cost
                n_coordinate = neighbor.coordinate
                if tentative_g_score < g_score.get(n_coordinate, 10000):
                    came_from[n_coordinate] = current
                    g_score[n_coordinate] = tentative_g_score
                    f_score[n_coordinate] = tentative_g_score + n_coordinate.distance(destination)
                    if n_coordinate not in open_set:
                        open_set.append(n_coordinate)
        return []

    @staticmethod
    def _reconstruct_path(hex_map: HexMap, came_from: Dict[HexCoordinate, HexCoordinate], current: HexCoordinate) -> List[HexCell]:
        path = [hex_map[current]]
        while current in came_from:
            current = came_from[current]
            path.append(hex_map[current])
        return path
