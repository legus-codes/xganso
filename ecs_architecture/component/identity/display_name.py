from ecs_architecture.component.registry import GlobalComponentRegistry
from omniecs.types import Component


class DisplayName(Component):
    name: str

@GlobalComponentRegistry.register_component('identity', 'name')
def build_display_name(name: str) -> DisplayName:
    return DisplayName(name=name)

test_config = {
    'cls': DisplayName,
    'builder': build_display_name,
    'parameters': {'name': 'display_name'},
    'fields': {'name': 'display_name'},
    'invalid_cases': [],
}
