from dataclasses import dataclass

from ecs_framework.ecs import ComponentProtocol


@dataclass
class AttackTarget(ComponentProtocol):
    entity: int


@dataclass
class AttackTargetDirty(ComponentProtocol):
    pass


@dataclass
class AttackCommand(ComponentProtocol):
    pass


@dataclass
class CombatPreview(ComponentProtocol):
    attacker: int
    attack: int
    defender: int
    defense: int
    damage: int


@dataclass
class CombatPreviewDirty(ComponentProtocol):
    pass


@dataclass
class AttackInstance(ComponentProtocol):
    attack: int


@dataclass
class IncomingDamage(ComponentProtocol):
    damage: int


@dataclass
class MarkedForDeath(ComponentProtocol):
    pass
