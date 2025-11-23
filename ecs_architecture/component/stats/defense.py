from pydantic import Field

from ecs_architecture.component.registry import GlobalComponentRegistry
from ecs_framework.ecs import ComponentProtocol


class Defense(ComponentProtocol):
    base: float = Field(ge=0)
    growth: float = Field(ge=0)

@GlobalComponentRegistry.register_component('stats.defense')
def build_defense(base: float, growth: float) -> Defense:
    return Defense(base=base, growth=growth)

test_config = {
    'cls': Defense,
    'builder': build_defense,
    'parameters': {'base': 18.4, 'growth': 4.2},
    'fields': {'base': 18.4, 'growth': 4.2},
    'invalid_cases': [
        {'base': -1, 'growth': 2},
        {'base': 1, 'growth': -2}
    ],
}
