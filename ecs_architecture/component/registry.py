from typing import Dict, Protocol, Tuple


class GlobalComponentRegistry:
    
    component_builders = {}

    @classmethod
    def get_section_component(cls, name: str) -> Tuple[str, str]:
        section, component = name.split('.')
        return section, component

    @classmethod
    def get_full_name(cls, section: str, component: str) -> str:
        return '.'.join([section, component])

    @classmethod
    def register_component(cls, name: str):
        def wrapper(fn: callable) -> callable:
            section, component = cls.get_section_component(name)
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

    def get_builder(self, section: str, component: str) -> callable:
        ...


class ComponentRegistry(ComponentRegistryProtocol):

    def __init__(self):
        self.builders: Dict[str, Dict[str, callable]] = {}

    def load(self, name: str) -> None:
        section, component = GlobalComponentRegistry.get_section_component(name)

        section_builders = GlobalComponentRegistry.get_section(section)
        if component not in section_builders:
            raise ValueError(f'Component {name} has no registered builder')

        if section not in self.builders:
            self.builders[section] = {}
        self.builders[section][component] = section_builders[component]
    
    def get_builder(self, section: str, component: str) -> callable:
        section_builders = self.builders.get(section, {})
        return section_builders.get(component, None)
