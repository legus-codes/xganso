from typing import Any, Dict, List

from ecs_architecture.component.registry import ComponentRegistryProtocol, GlobalComponentRegistry
from ecs_framework.ecs import ComponentProtocol


class ComponentBuilder:
    
    def __init__(self, registry: ComponentRegistryProtocol):
        self.registry = registry

    def build(self, data: Dict[str, Dict[str, Any]]) -> List[ComponentProtocol]:
        ecs_components = []
        for section, components in data.items():
            for component, kwargs in components.items():
                ecs_components.append(self._build_component(section, component, kwargs))
        return ecs_components

    def _build_component(self, section: str, component: str, kwargs: Any) -> ComponentProtocol:
        builder_fn = self.registry.get_builder(section, component)
        if builder_fn is None:
            raise KeyError(f'No builder registered for {GlobalComponentRegistry.get_full_name(section, component)}')

        return builder_fn(**kwargs)
