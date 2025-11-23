from ecs_architecture.component.registry import GlobalComponentRegistry
from ecs_framework.ecs import ComponentProtocol


class Identifier(ComponentProtocol):
    identity: str

@GlobalComponentRegistry.register_component('identity.id')
def build_identifier(identity: str) -> Identifier:
    return Identifier(identity=identity)

test_config = {
    'cls': Identifier,
    'builder': build_identifier,
    'parameters': {'identity': 'id'},
    'fields': {'identity': 'id'},
    'invalid_cases': [],
}
