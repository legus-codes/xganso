from pygame import Surface

from ecs_architecture.component.registry import register_component
from ecs_framework.ecs import ComponentProtocol


class Sprite(ComponentProtocol):
    sprite: Surface


class UnitSprite(ComponentProtocol):
    character: str 
    board: str

@register_component('sprite')
def build_unit_sprite(character: str, board: str) -> UnitSprite:
    return UnitSprite(character=character, board=board)


class ScreenSprite(ComponentProtocol):
    sprite: Surface
