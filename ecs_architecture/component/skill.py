from ecs_architecture.component.registry import GlobalComponentRegistry
from ecs_framework.ecs import ComponentProtocol


class PassiveSkill(ComponentProtocol):
    name: str

@GlobalComponentRegistry.register_component('skills.passive')
def build_passive_skill(name: str) -> PassiveSkill:
    return PassiveSkill(name=name)
