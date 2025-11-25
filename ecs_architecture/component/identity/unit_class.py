from ecs_architecture.component.registry import GlobalComponentRegistry
from ecs_framework.ecs import ComponentProtocol


class UnitClass(ComponentProtocol):
    unit_class: str

@GlobalComponentRegistry.register_component('identity', 'unit_class')
def build_unit_class(unit_class: str) -> UnitClass:
    return UnitClass(unit_class=unit_class)

test_config = {
    'cls': UnitClass,
    'builder': build_unit_class,
    'parameters': {'unit_class': 'unit_class'},
    'fields': {'unit_class': 'unit_class'},
    'invalid_cases': [],
}
