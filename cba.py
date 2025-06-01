from dataclasses import dataclass
import random
from typing import Protocol

import pygame



class ComponentProtocol(Protocol):

    parent: 'Object'

    def update(self) -> None:
        ...


class Renderer(ComponentProtocol):

    def __init__(self, sprite, screen: pygame.Surface):
        self.sprite = sprite
        self.screen = screen

    def update(self):
        movement = self.parent.get_component(Movement)
        if not movement:
            return

        self.screen.blit(self.sprite, movement.position)


class Movement(ComponentProtocol):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    @property
    def position(self):
        return (self.x, self.y)

    def update(self):
        pass


class Combat:
    
    def __init__(self, hp, attack, defense):
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defense = defense

    def deal_damage(self, target):
        target.get_component(Combat).take_damage(self.attack)

    def take_damage(self, amount):
        damage = max(0, amount - self.defense)
        self.hp = max(0, self.hp - damage)
        print(f'{self.parent.id} took {damage} damage (HP: {self.hp}/{self.max_hp})')

    @property
    def alive(self):
        return self.hp > 0
    
    def update(self):
        pass


class LevelProgression(ComponentProtocol):

    def __init__(self, level, xp):
        self.level = level
        self.xp = xp
        self.base_xp_to_next_level = 100

    def xp_to_next_level(self):
        return self.base_xp_to_next_level + (self.level - 1) * 50

    def gain_xp(self, amount):
        self.xp += amount
        while self.xp >= self.xp_to_next_level():
            self.xp -= self.xp_to_next_level()
            self.level_up()

    def level_up(self):
        self.level += 1
        print(f'{self.parent.id} leveled up! Now level {self.level}')

    def update(self):
        pass


@dataclass
class Skill:
    name: str
    required_level: int


class SkillTree(ComponentProtocol):

    def __init__(self, skills):
        self.skills = {skill.name: skill for skill in skills}
        self.unlocked = set()

    def can_unlock(self, skill_name):
        skill = self.skills.get(skill_name)
        if not skill or self.has_skill(skill.name):
            return False
        
        progression = self.parent.get_component(LevelProgression)
        if not progression or progression.level < skill.required_level:
            return False
        
        return True

    def unlock(self, skill_name):
        if self.can_unlock(skill_name):
            self.unlocked.add(skill_name)
            print(f'{self.parent.id} unlocked skill: {skill_name}')
            return True
        return False
    
    def has_skill(self, skill_name):
        return skill_name in self.unlocked

    def update(self):
        pass


class Object:

    _id_counter = 0

    def __init__(self):
        self.id = Object._id_counter
        Object._id_counter += 1
        self.components = {}

    def add_component(self, component: ComponentProtocol):
        self.components[component.__class__] = component
        component.parent = self

    def get_component(self, component_class):
        return self.components.get(component_class, None)
    
    def update(self):
        for component in self.components.values():
            component.update()


pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()


sprite = pygame.Surface((50, 50))
sprite.fill((255, 0, 0))

character = Object()
renderer = Renderer(sprite, screen)
movement = Movement(100, 100)
combat = Combat(30, 8, 2)
level = LevelProgression(1, 0)
skills = [
    Skill('Fire Ball', required_level=2),
    Skill('Ice Wave', required_level=3),
    Skill('Thunder Strike', required_level=4),
]
skill_tree = SkillTree(skills)

character.add_component(renderer)
character.add_component(movement)
character.add_component(combat)
character.add_component(level)
character.add_component(skill_tree)

opponent = Object()
enemy_combat = Combat(20, 5, 1)
opponent.add_component(enemy_combat)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                x = random.randint(0, 640)
                y = random.randint(0, 480)
                character.get_component(Movement).move(x, y)

            if event.key == pygame.K_a:
                character.get_component(Combat).deal_damage(opponent)

            if event.key == pygame.K_x:
                character.get_component(LevelProgression).gain_xp(80)

            if event.key == pygame.K_u:
                for skill in skills:
                    character.get_component(SkillTree).unlock(skill.name)

        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    character.update()
    pygame.display.flip()

pygame.quit()


