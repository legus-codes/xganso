from pydantic import Field

from ecs_architecture.component.registry import GlobalComponentRegistry
from ecs_framework.ecs import ComponentProtocol


class HP(ComponentProtocol):
    current: float = Field(ge=0)
    max_value: float = Field(ge=0)
    regeneration: float = Field(ge=0)
    growth: float = Field(ge=0)

@GlobalComponentRegistry.register_component('stats', 'hp')
def build_hp(base: float, regen: float, growth: float) -> HP:
    return HP(current=base, max_value=base, regeneration=regen, growth=growth)

test_config = {
    'cls': HP,
    'builder': build_hp,
    'parameters': {'base': 10.4, 'growth': 3.5, 'regen': 6.4},
    'fields': {'current': 10.4, 'max_value': 10.4, 'growth': 3.5, 'regeneration': 6.4},
    'invalid_cases': [
        {'base': -1, 'growth': 2, 'regen': 3},
        {'base': 1, 'growth': -2, 'regen': 3},
        {'base': 1, 'growth': -2, 'regen': -3}
    ],
}
