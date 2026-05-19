from ecs_architecture.component.registry import GlobalComponentRegistry
from omniecs.types import Component


class UnitBoardSprite(Component):
    path: str

@GlobalComponentRegistry.register_component('sprites', 'board')
def build_unit_sprite(path: str) -> UnitBoardSprite:
    return UnitBoardSprite(path=path)

test_config = {
    'cls': UnitBoardSprite,
    'builder': build_unit_sprite,
    'parameters': {'path': 'path'},
    'fields': {'path': 'path'},
    'invalid_cases': [],
}
