from typing import List

from ecs_architecture.component.registry import ComponentRegistryProtocol
from ecs_framework.ecs import ComponentProtocol


class ComponentBuilder:
    
    def __init__(self, registry: ComponentRegistryProtocol):
        self.registry = registry

    def build(self, data: dict) -> List[ComponentProtocol]:
        components = []
        for name, kwargs in data.items():
            builder_fn = self.registry.get_builder(name)
            if builder_fn is None:
                raise KeyError(f'No builder registered for {name}')
            components.append(builder_fn(**kwargs))
        return components
