from typing import Dict, List
import pygame
from model.hex_coordinate import HexCoordinate


class Unit:

    def __init__(self, name: str, hp: int, attack: int, attack_range: int, movement_range: int, color: pygame.Color):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.attack_range = attack_range
        self.position = None
        self.movement_range = movement_range
        self.color = color
        self.party: "Party" = None

    def move(self, position: HexCoordinate) -> None:
        self.position = position

    def take_damage(self, damage: int) -> None:
        self.hp -= damage
    

class Party:

    def __init__(self, name: str, color: str, members: List[Unit], is_human: bool):
        self.name = name
        self.color = color
        self.is_human = is_human
        self.members: Dict[str, Unit] = {}
        for member in members:
            self.add_member(member)

    def add_member(self, member: Unit) -> None:
        member.party = self
        self.members[member.name] = member

    def remove_member(self, member: Unit) -> None:
        member.party = None
        self.members.pop(member)
        
    @property
    def count(self) -> int:
        return len(self.members)
