from typing import Protocol


COMPONENT_BUILDERS = {}

def register_component(name: str):
    def wrapper(fn: callable) -> callable:
        if name in COMPONENT_BUILDERS:
            raise ValueError(f'Component {name} already registered')
        COMPONENT_BUILDERS[name] = fn
        return fn
    return wrapper


class ComponentRegistryProtocol(Protocol):

    def get_builder(self, name: str) -> callable:
        ...


class ComponentRegistry(ComponentRegistryProtocol):

    def __init__(self):
        self.builders = {}

    def load(self, name: str) -> None:
        if name not in COMPONENT_BUILDERS: 
            raise ValueError(f'Component {name} has no registered builder')
        self.builders[name] = COMPONENT_BUILDERS[name]
    
    def get_builder(self, name: str) -> callable:
        return self.builders.get(name, None)
