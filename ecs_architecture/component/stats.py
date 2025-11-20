from pydantic import Field

from ecs_architecture.component.registry import register_component
from ecs_framework.ecs import ComponentProtocol


class Attack(ComponentProtocol):
    base: float = Field(ge=0)
    growth: float = Field(ge=0)

@register_component('attack')
def build_attack(base: float, growth: float) -> Attack:
    return Attack(base=base, growth=growth)


class Defense(ComponentProtocol):
    base: float = Field(ge=0)
    growth: float = Field(ge=0)

@register_component('defense')
def build_defense(base: float, growth: float) -> Defense:
    return Defense(base=base, growth=growth)


class HP(ComponentProtocol):
    current: float = Field(ge=0)
    max_value: float = Field(ge=0)
    regeneration: float = Field(ge=0)
    growth: float = Field(ge=0)

@register_component('hp')
def build_hp(base: float, regen: float, growth: float) -> HP:
    return HP(current=base, max_value=base, regeneration=regen, growth=growth)
