from ecs_architecture.component.registry import GlobalComponentRegistry
from ecs_framework.ecs import ComponentProtocol


class Identity(ComponentProtocol):
    identity: str

@GlobalComponentRegistry.register_component('identification.id')
def build_identity(identity: str) -> Identity:
    return Identity(identity=identity)


class DisplayName(ComponentProtocol):
    name: str

@GlobalComponentRegistry.register_component('identification.name')
def build_display_name(name: str) -> DisplayName:
    return DisplayName(name=name)


class UnitClass(ComponentProtocol):
    unit_classe: str

@GlobalComponentRegistry.register_component('identification.unit_class')
def build_unit_class(unit_class: str) -> UnitClass:
    return UnitClass(unit_class=unit_class)
