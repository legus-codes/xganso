from pydantic import Field

from ecs_architecture.component.registry import GlobalComponentRegistry
from omniecs.types import Component


class AttackRange(Component):
    base: float = Field(ge=0)

@GlobalComponentRegistry.register_component('stats', 'attack_range')
def build_attack_range(base: float) -> AttackRange:
    return AttackRange(base=base)

test_config = {
    'cls': AttackRange,
    'builder': build_attack_range,
    'parameters': {'base': 5},
    'fields': {'base': 5},
    'invalid_cases': [
        {'base': -1}
    ],
}
