from dataclasses import dataclass
import math

from ecs_architecture.component.stats import HP, Attack, Defense
from ecs_framework.ecs import ECS, ComponentProtocol, SystemProtocol


@dataclass
class XP(ComponentProtocol):
    current: int
    needed: int
    total: int
    growth: float


@dataclass
class XPGained(ComponentProtocol):
    amount: int


@dataclass
class Level(ComponentProtocol):
    current: int


@dataclass
class LevelUp(ComponentProtocol):
    amount: int


class GainXP(SystemProtocol):
    
    def __init__(self, ecs: ECS):
        self.ecs = ecs

    def execute(self, delta_time: float):
        for entity, xp_gained in self.ecs.get_entities_with_single_component(XPGained):
            xp: XP = self.ecs.get_entity_component(entity, XP)
            if xp is not None:
                xp.total += xp_gained.amount

                while xp_gained.amount >= xp.needed - xp.current:
                    xp_gained.amount -= (xp.needed - xp.current)
                    xp.current = 0
                    xp.needed = math.floor(xp.needed * xp.growth)
                    level_up = self.ecs.get_entity_component(entity, LevelUp)
                    if level_up is None:
                        self.ecs.add_component(entity, LevelUp(1))
                    else:
                        level_up.amount += 1

                xp.current += xp_gained.amount
            
            self.ecs.remove_component(entity, XPGained)


class IncreaseLevel(SystemProtocol):
    
    def __init__(self, ecs: ECS):
        self.ecs = ecs

    def execute(self, delta_time: float):
        for entity, level_up in self.ecs.get_entities_with_single_component(LevelUp):
            level: Level = self.ecs.get_entity_component(entity, Level)

            if level is not None:
                for _ in range(level_up.amount):
                    level.current += 1
                    attack: Attack = self.ecs.get_entity_component(entity, Attack)
                    attack.base += attack.growth
                    defense: Defense = self.ecs.get_entity_component(entity, Defense)
                    defense.base += defense.growth
                    hp: HP = self.ecs.get_entity_component(entity, HP)
                    hp.max_value += hp.growth
                    hp.current = hp.max_value

            self.ecs.remove_component(entity, LevelUp)
