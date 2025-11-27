from typing import Any, Dict, List, Protocol

from ecs_architecture.component.registry import ComponentRegistryProtocol
from ecs_framework.ecs import ComponentProtocol


class ComponentBuilderProtocol(Protocol):

    def build(self, data: Dict[str, Dict[str, Any]]) -> List[ComponentProtocol]:
        ...


class ComponentBuilder(ComponentBuilderProtocol):
    
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
            raise KeyError(f'No builder registered for {section} {component}')

        return builder_fn(**kwargs)
