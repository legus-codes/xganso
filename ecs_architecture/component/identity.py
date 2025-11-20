from ecs_architecture.component.registry import register_component
from ecs_framework.ecs import ComponentProtocol


class Identity(ComponentProtocol):
    identity: str

@register_component('id')
def build_identity(identity: str) -> Identity:
    return Identity(identity=identity)


class DisplayName(ComponentProtocol):
    name: str

@register_component('name')
def build_display_name(name: str) -> DisplayName:
    return DisplayName(name=name)


class UnitClass(ComponentProtocol):
    unit_classe: str

@register_component('unit_class')
def build_unit_class(unit_class: str) -> UnitClass:
    return UnitClass(unit_class=unit_class)
