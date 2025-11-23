from pydantic import Field

from ecs_architecture.component.registry import GlobalComponentRegistry
from ecs_framework.ecs import ComponentProtocol


class Speed(ComponentProtocol):
    base: float = Field(ge=0)
    growth: float = Field(ge=0)

@GlobalComponentRegistry.register_component('stats.speed')
def build_speed(base: float, growth: float) -> Speed:
    return Speed(base=base, growth=growth)

test_config = {
    'cls': Speed,
    'builder': build_speed,
    'parameters': {'base': 3.0, 'growth': 0.75},
    'fields': {'base': 3.0, 'growth': 0.75},
    'invalid_cases': [
        {'base': -1, 'growth': 2},
        {'base': 1, 'growth': -2}
    ],
}
