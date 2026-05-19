from ecs_architecture.component.registry import GlobalComponentRegistry
from omniecs.types import Component


class UnitCharacterSprite(Component):
    path: str 

@GlobalComponentRegistry.register_component('sprites', 'character')
def build_unit_sprite(path: str) -> UnitCharacterSprite:
    return UnitCharacterSprite(path=path)

test_config = {
    'cls': UnitCharacterSprite,
    'builder': build_unit_sprite,
    'parameters': {'path': 'path'},
    'fields': {'path': 'path'},
    'invalid_cases': [],
}
