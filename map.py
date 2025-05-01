from typing import List
from model.hex_map import HexCell, HexMap
import random


class BattleMap:

    def __init__(self, grid: HexMap, starting_positions: List[List[HexCell]]):
        self.grid = grid
        self.starting_positions = starting_positions

    def get_starting_positions(self, team_members_a: int, team_members_b: int) -> List[List[HexCell]]:
        if random.choice([True, False]):
            team_a_positions = self.select_positions(self.starting_positions[0], team_members_a)
            team_b_positions = self.select_positions(self.starting_positions[1], team_members_b)
        else:
            team_a_positions = self.select_positions(self.starting_positions[1], team_members_a)
            team_b_positions = self.select_positions(self.starting_positions[0], team_members_b)
        return [team_a_positions, team_b_positions]
    
    def select_positions(self, positions: List[HexCell], amount: int) -> List[HexCell]:
        return random.sample(positions, k=amount)
    
