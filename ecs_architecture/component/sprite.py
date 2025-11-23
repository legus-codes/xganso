from pygame import Surface

from ecs_architecture.component.registry import GlobalComponentRegistry
from ecs_framework.ecs import ComponentProtocol


class Sprite(ComponentProtocol):
    sprite: Surface


class UnitCharacterSprite(ComponentProtocol):
    path: str 

@GlobalComponentRegistry.register_component('sprites.character')
def build_unit_sprite(path: str) -> UnitCharacterSprite:
    return UnitCharacterSprite(path=path)


class UnitBoardSprite(ComponentProtocol):
    path: str

@GlobalComponentRegistry.register_component('sprites.board')
def build_unit_sprite(path: str) -> UnitBoardSprite:
    return UnitBoardSprite(path=path)


class ScreenSprite(ComponentProtocol):
    sprite: Surface
