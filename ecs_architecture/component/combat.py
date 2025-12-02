from ecs_framework.ecs import ComponentProtocol


class AttackTarget(ComponentProtocol):
    entity: int


class AttackTargetDirty(ComponentProtocol):
    pass


class AttackCommand(ComponentProtocol):
    pass


class CombatPreview(ComponentProtocol):
    attacker: int
    attack: int
    defender: int
    defense: int
    damage: int


class CombatPreviewDirty(ComponentProtocol):
    pass


class AttackInstance(ComponentProtocol):
    attack: int


class IncomingDamage(ComponentProtocol):
    damage: int


class MarkedForDeath(ComponentProtocol):
    pass
