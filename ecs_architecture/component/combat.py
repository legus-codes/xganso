from omniecs.types import Component


class AttackTarget(Component):
    entity: int


class AttackTargetDirty(Component):
    pass


class AttackCommand(Component):
    pass


class CombatPreview(Component):
    attacker: int
    attack: int
    defender: int
    defense: int
    damage: int


class CombatPreviewDirty(Component):
    pass


class AttackInstance(Component):
    attack: int


class IncomingDamage(Component):
    damage: int


class MarkedForDeath(Component):
    pass
