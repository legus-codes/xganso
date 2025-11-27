from typing import Dict, List, Protocol


class GlobalComponentRegistry:
    
    component_builders = {}

    @classmethod
    def register_component(cls, section: str, component: str):
        def wrapper(fn: callable) -> callable:
            if section not in cls.component_builders:
                cls.component_builders[section] = {}
            
            if component in cls.component_builders[section]:
                raise ValueError(f'Component {component} already registered in section {section}')
            cls.component_builders[section][component] = fn
            return fn
        return wrapper
    
    @classmethod
    def get_section(cls, name: str) -> Dict[str, callable]:
        return cls.component_builders.get(name, {})
    

class ComponentRegistryProtocol(Protocol):

    def load_all(self, data: Dict[str, List[str]]) -> None:
        ...

    def load(self, section: str, component: str) -> None:
        ...

    def get_builder(self, section: str, component: str) -> callable:
        ...


class ComponentRegistry(ComponentRegistryProtocol):

    def __init__(self):
        self.builders: Dict[str, Dict[str, callable]] = {}

    def load_all(self, data: Dict[str, List[str]]) -> None:
        for section, components in data.items():
            for component in components:
                self.load(section, component)

    def load(self, section: str, component: str) -> None:
        section_builders = GlobalComponentRegistry.get_section(section)
        if component not in section_builders:
            raise ValueError(f'Component {section} {component} has no registered builder')

        if section not in self.builders:
            self.builders[section] = {}
        self.builders[section][component] = section_builders[component]
    
    def get_builder(self, section: str, component: str) -> callable:
        section_builders = self.builders.get(section, {})
        return section_builders.get(component, None)
