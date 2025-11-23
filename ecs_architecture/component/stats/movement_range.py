from pydantic import Field

from ecs_architecture.component.registry import GlobalComponentRegistry
from ecs_framework.ecs import ComponentProtocol


class MovementRange(ComponentProtocol):
    base: float = Field(ge=0)

@GlobalComponentRegistry.register_component('stats.movement_range')
def build_movement_range(base: float) -> MovementRange:
    return MovementRange(base=base)

test_config = {
    'cls': MovementRange,
    'builder': build_movement_range,
    'parameters': {'base': 8},
    'fields': {'base': 8},
    'invalid_cases': [
        {'base': -1}
    ],
}
