from pydantic import Field

from ecs_architecture.component.registry import GlobalComponentRegistry
from ecs_framework.ecs import ComponentProtocol


class Attack(ComponentProtocol):
    base: float = Field(ge=0)
    growth: float = Field(ge=0)

@GlobalComponentRegistry.register_component('stats.attack')
def build_attack(base: float, growth: float) -> Attack:
    return Attack(base=base, growth=growth)

test_config = {
    'cls': Attack,
    'builder': build_attack,
    'parameters': {'base': 10.4, 'growth': 3.5},
    'fields': {'base': 10.4, 'growth': 3.5},
    'invalid_cases': [
        {'base': -1, 'growth': 2},
        {'base': 1, 'growth': -2}
    ],
}
