from itertools import count
from typing import Any, Dict, Generator, List, Protocol, Set, Tuple

from pydantic import BaseModel


class ComponentProtocol(BaseModel):
    ...


class SystemProtocol(Protocol):

    def execute(self, delta_time: float) -> None:
        ...


class ECS:

    def __init__(self) -> None:
        self._next_entity_id = count()
        self.entities: Set[int] = set()
        self.world: Dict[type, Dict[int, ComponentProtocol]] = {}
        self.systems: list = []
        self.running = True

    def reset(self) -> None:
        self.entities.clear()
        self.world.clear()
        self.systems.clear()

    def has_entity(self, entity_id: int) -> bool:
        return entity_id in self.entities
    
    def entity_has_component(self, entity_id: int, component_type: type) -> bool:
        return self.has_component(component_type) and entity_id in self.world[component_type]

    def has_component(self, component_type: type) -> bool:
        return component_type in self.world

    def has_system(self, system: Any) -> bool:
        return system in self.systems

    def create_entity(self) -> int:
        entity_id = next(self._next_entity_id)
        self.entities.add(entity_id)
        return entity_id
    
    def delete_entity(self, entity_id: int) -> None:
        if not self.has_entity(entity_id):
            return
        
        self.entities.remove(entity_id)
        for component in self.world.values():
            if entity_id in component:
                component.pop(entity_id)

    def add_component(self, entity_id: int, component: ComponentProtocol) -> None:
        if not self.has_entity(entity_id):
            return

        component_type = type(component)
        if component_type not in self.world:
            self.world[component_type] = {}
            
        self.world[component_type][entity_id] = component

    def remove_component(self, entity_id: int, component_type: type) -> None:
        if self.get_entity_component(entity_id, component_type) is None:
            return
        
        self.world[component_type].pop(entity_id)

    def get_entity_component(self, entity_id: int, component_type: type) -> ComponentProtocol:
        if not self.has_component(component_type):
            return None
        
        if not self.entity_has_component(entity_id, component_type):
            return None
        
        return self.world[component_type][entity_id]

    def get_all_entity_components(self, entity_id: int) -> List[ComponentProtocol]:
        if not self.has_entity(entity_id):
            return None
        
        entity_components = []
        for component in self.world.keys():
            entity_components.append(self.get_entity_component(entity_id, component))
        return entity_components

    def get_entities_with(self, *component_types) -> List[int]:
        if not component_types:
            return []

        eligible_entities = {}
        for component_type in component_types:
            if not self.has_component(component_type):
                return []
            
            eligible_entities[component_type] = set(self.world[component_type].keys())

        return list(set.intersection(*eligible_entities.values()))

    def get_entities_with_single_component(self, component_type) -> Generator[int, ComponentProtocol]:
        for entity in self.get_entities_with(component_type):
            yield entity, self.get_entity_component(entity, component_type)

    def get_entities_with_components(self, *component_types) -> Generator[int, Tuple[ComponentProtocol]]:
        for entity in self.get_entities_with(*component_types):
            yield entity, (self.get_entity_component(entity, component) for component in component_types)

    def add_system(self, system: Any) -> None:
        self.systems.append(system)

    def execute(self, delta_time: float) -> None:
        for system in self.systems:
            system.execute(delta_time)
