from ecs_architecture.component.combat import AttackCommand, AttackInstance, AttackTarget, AttackTargetDirty, CombatPreview, CombatPreviewDirty, IncomingDamage, MarkedForDeath
from ecs_architecture.component.stats import HP, Attack, Defense
from ecs_framework.ecs import ECS, SystemProtocol


class CombatSimulatorSystem(SystemProtocol):

    def __init__(self, ecs: ECS):
        self.ecs = ecs

    def execute(self, delta_time: int):
        for entity, _ in self.ecs.get_entities_with_single_component(AttackTargetDirty):
            target = self.ecs.get_entity_component(entity, AttackTarget)

            if target:
                attack = self.ecs.get_entity_component(entity, Attack).base
                defense = self.ecs.get_entity_component(target.entity, Defense).base
                damage = attack - defense
                self.ecs.add_component(entity, CombatPreview(entity, attack, target.entity, defense, damage))
                self.ecs.add_component(entity, CombatPreviewDirty())

            self.ecs.remove_component(entity, AttackTargetDirty)


class CombatPreviewerSystem(SystemProtocol):

    def __init__(self, ecs: ECS):
        self.ecs = ecs

    def execute(self, delta_time):
        for entity, _ in self.ecs.get_entities_with_single_component(CombatPreviewDirty):
            combat_preview = self.ecs.get_entity_component(entity, CombatPreview)

            if combat_preview:
                print('Combat Preview')
                print(f'Attacker: {combat_preview.attacker} ({combat_preview.attack})')
                print(f'Defender: {combat_preview.defender} ({combat_preview.defense})')
                print(f'Damage: {combat_preview.damage}')

            self.ecs.remove_component(entity, CombatPreviewDirty)


class AttackTriggerSystem(SystemProtocol):

    def __init__(self, ecs: ECS):
        self.ecs = ecs

    def execute(self, delta_time):
        for entity, _ in self.ecs.get_entities_with_single_component(AttackCommand):
            self.ecs.remove_component(entity, CombatPreview)
            target = self.ecs.get_entity_component(entity, AttackTarget)

            if target:
                attack = self.ecs.get_entity_component(entity, Attack).base
                self.ecs.add_component(target.entity, AttackInstance(attack))
                print(f'{entity} attacked {target.entity} with power {attack}')

            self.ecs.remove_component(entity, AttackCommand)


class AttackResolutionSystem(SystemProtocol):

    def __init__(self, ecs: ECS):
        self.ecs = ecs

    def execute(self, delta_time):
        for entity, attack_instance in self.ecs.get_entities_with_single_component(AttackInstance):
            defense = self.ecs.get_entity_component(entity, Defense).base

            damage = attack_instance.attack - defense
            self.ecs.add_component(entity, IncomingDamage(damage))
            print(f'{entity} blocked attack with power {attack_instance} with defense {defense} resulting in {damage} damage')

            self.ecs.remove_component(entity, AttackInstance)


class DamageApplicationSystem(SystemProtocol):

    def __init__(self, ecs: ECS):
        self.ecs = ecs

    def execute(self, delta_time):
        for entity, incoming_damage in self.ecs.get_entities_with_single_component(IncomingDamage):
            hp = self.ecs.get_entity_component(entity, HP)

            hp.current -= incoming_damage.damage
            print(f'{entity} took {incoming_damage.damage} damage. It is now with {hp.current} hp')
            if hp.current <= 0:
                self.ecs.add_component(entity, MarkedForDeath())
                print(f'{entity} does not have hp')

            self.ecs.remove_component(entity, IncomingDamage)


class DeathSystem(SystemProtocol):

    def __init__(self, ecs: ECS):
        self.ecs = ecs

    def execute(self, delta_time):
        for entity, _ in self.ecs.get_entities_with_single_component(MarkedForDeath):
            print(f'{entity} died')
            self.ecs.remove_component(entity, MarkedForDeath)
