from dataclasses import dataclass
import itertools
import random
from typing import Dict, Protocol, Set

import pygame



@dataclass
class PositionComponent:
    x: int
    y: int


@dataclass
class RenderComponent:
    sprite: pygame.Surface
    screen: pygame.Surface


@dataclass
class CombatComponent:
    hp: int
    max_hp: int
    attack: int
    defense: int


@dataclass
class LevelComponent:
    xp: int = 0
    level: int = 1
    base_xp_to_next_level: int = 100


@dataclass
class Skill:
    name: str
    required_level: int


@dataclass
class SkillTreeComponent:
    skills: Dict[str, Skill]
    unlocked: Set[str]


class System(Protocol):
    ecs: 'ECS'

    def update(self):
        ...


class RenderSystem(System):

    def update(self):
        for entity in self.ecs.get_entities_with(RenderComponent, PositionComponent):
            position = self.ecs.get_component(entity, PositionComponent)
            renderer = self.ecs.get_component(entity, RenderComponent)
            renderer.screen.blit(renderer.sprite, (position.x, position.y))


class MovementSystem(System):

    def move(self, entity, new_x, new_y):
        position = self.ecs.get_component(entity, PositionComponent)
        if not position:
            return
        position.x = new_x
        position.y = new_y


class CombatSystem(System):
    
    def deal_damage(self, attacker_entity, target_entity):
        attacker = self.ecs.get_component(attacker_entity, CombatComponent)
        target = self.ecs.get_component(target_entity, CombatComponent)
        if attacker and target:
            damage = max(0, attacker.attack - target.defense)
            target.hp = max(0, target.hp - damage)
            print(f'Entity {target_entity} took {damage} damage (HP: {target.hp}/{target.max_hp})')


class LevelSystem(System):

    def gain_xp(self, entity, amount):
        level = self.ecs.get_component(entity, LevelComponent)
        if not level:
            return
        
        level.xp += amount
        while level.xp >= self.xp_to_next(level):
            level.xp -= self.xp_to_next(level)
            level.level += 1
            print(f'Entity {entity} leveled up to {level.level}')

    def xp_to_next(self, level):
        return level.base_xp_to_next_level + (level.level - 1) * 50


class SkillSystem(System):

    def unlock(self, entity, skill_name):
        tree = self.ecs.get_component(entity, SkillTreeComponent)
        level = self.ecs.get_component(entity, LevelComponent)
        if not tree or not level:
            return
        
        skill = tree.skills.get(skill_name)
        if not skill or skill_name in tree.unlocked or level.level < skill.required_level:
            return
        
        tree.unlocked.add(skill_name)
        print(f'Entity {entity} unlocked skill: {skill_name}')


class ECS:

    def __init__(self):
        self._next_entity_id = itertools.count()
        self.components = {}
        self.systems = []

    def create_entity(self):
        return next(self._next_entity_id)
    
    def add_component(self, entity, component):
        ctype = type(component)
        if ctype not in self.components:
            self.components[ctype] = {}
        self.components[ctype][entity] = component

    def get_component(self, entity, component_type):
        return self.components.get(component_type, {}).get(entity)
    
    def get_entities_with(self, *component_types):
        if not component_types:
            return set()
        sets = [set(self.components.get(ctype, {}).keys()) for ctype in component_types]
        return set.intersection(*sets)

    def add_system(self, system):
        self.systems.append(system)

    def update(self):
        for system in self.systems:
            system.update()


pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

sprite = pygame.Surface((50, 50))
sprite.fill((255, 0, 0))

ecs = ECS()

skills = {
    'Fire Ball': Skill('Fire Ball', required_level=2),
    'Ice Wave': Skill('Ice Wave', required_level=3),
    'Thunder Strike': Skill('Thunder Strike', required_level=4),
}

player = ecs.create_entity()
ecs.add_component(player, PositionComponent(100, 100))
ecs.add_component(player, RenderComponent(sprite, screen))
ecs.add_component(player, CombatComponent(30, 30, 8, 2))
ecs.add_component(player, LevelComponent())
ecs.add_component(player, SkillTreeComponent(skills, set()))

render_system = RenderSystem()
render_system.ecs = ecs
movement_system = MovementSystem()
movement_system.ecs = ecs
combat_system = CombatSystem()
combat_system.ecs = ecs
level_system = LevelSystem()
level_system.ecs = ecs
skill_system = SkillSystem()
skill_system.ecs = ecs
ecs.add_system(render_system)
ecs.add_system(movement_system)
ecs.add_system(combat_system)
ecs.add_system(level_system)
ecs.add_system(skill_system)

opponent = ecs.create_entity()
ecs.add_component(opponent, CombatComponent(20, 20, 5, 1))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                x = random.randint(0, 640)
                y = random.randint(0, 480)
                movement_system.move(player, x, y)

            if event.key == pygame.K_a:
                combat_system.deal_damage(player, opponent)

            if event.key == pygame.K_x:
                level_system.gain_xp(player, 80)

            if event.key == pygame.K_u:
                for skill in skills.values():
                    skill_system.unlock(player, skill.name)

        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    ecs.update()
    pygame.display.flip()

pygame.quit()
