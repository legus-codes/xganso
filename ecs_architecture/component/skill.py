from ecs_architecture.component.registry import register_component
from ecs_framework.ecs import ComponentProtocol


class PassiveSkill(ComponentProtocol):
    name: str

@register_component('passive')
def build_passive_skill(name: str) -> PassiveSkill:
    return PassiveSkill(name=name)
