from collections import defaultdict
from itertools import chain, count
from typing import Iterable

from ecs_framework.system import System
from ecs_framework.types import R, Component, Cs, DrawCommandProtocol, EntityId, Event, ExecutionStage, Resource


class EntityManager:

    def __init__(self):
        self._next_entity_id = count()
        self._entities: set[EntityId] = set()

    def create(self) -> EntityId:
        entity_id = EntityId(next(self._next_entity_id))
        self._entities.add(entity_id)
        return entity_id
    
    def destroy(self, entity_id: EntityId) -> None:
        self._entities.discard(entity_id)

    def exists(self, entity_id: EntityId) -> bool:
        return entity_id in self._entities


class ComponentStorage[C: Component]:

    def __init__(self):
        self._components: dict[EntityId, C] = {}

    def add(self, entity_id: EntityId, component: C) -> None:
        self._components[entity_id] = component

    def remove(self, entity_id: EntityId) -> None:
        self._components.pop(entity_id, None)

    def get(self, entity_id: EntityId) -> C | None:
        return self._components.get(entity_id, None)

    def has(self, entity_id: EntityId) -> bool:
        return entity_id in self._components

    def entities(self) -> set[EntityId]:
        return set(self._components.keys())


class ComponentManager:

    def __init__(self):
        self._component_storage: dict[type[Component], ComponentStorage[Component]] = defaultdict(ComponentStorage)
        self._temporary_components: list[type[Component]] = []

    def add(self, entity_id: EntityId, component: Component) -> None:
        self._component_storage[type(component)].add(entity_id, component)

    def remove(self, entity_id: EntityId, component_type: type[Component]) -> None:
        self._component_storage.get(component_type, ComponentStorage()).remove(entity_id)

    def remove_all(self, component_type: type[Component]) -> None:
        self._component_storage.pop(component_type, None)

    def destroy(self, entity_id: EntityId) -> None:
        for storage in self._component_storage.values():
            storage.remove(entity_id)

    def has(self, entity_id: EntityId, component_type: type[Component]) -> bool:
        return component_type in self._component_storage and self._component_storage[component_type].has(entity_id)

    def query_entities(self,
                       all_of: tuple[type[Component], ...] = (),
                       any_of: tuple[type[Component], ...] = (),
                       none_of: tuple[type[Component], ...] = ()
     ) -> set[EntityId]:
        if len(self._component_storage) == 0:
            return set()

        entities = set.union(*(storage.entities() for storage in self._component_storage.values()))

        if all_of:
            for component in all_of:
                entities.intersection_update(self._component_storage[component].entities())
            if not entities:
                return entities

        if any_of:
            candidates = set.union(*(self._component_storage[c].entities() for c in any_of if c in self._component_storage))
            entities.intersection_update(candidates)
            if not entities:
                return entities

        if none_of:
            candidates = set.union(*(self._component_storage[c].entities() for c in none_of if c in self._component_storage))
            entities.difference_update(candidates)

        return entities

    def query(self,
              *component_types: *Cs,
              all_of: tuple[type[Component], ...] = (),
              any_of: tuple[type[Component], ...] = (),
              none_of: tuple[type[Component], ...] = ()
     ) -> Iterable[tuple[EntityId, tuple[*Cs]]]:
        entities = self.query_entities(all_of + component_types, any_of, none_of)

        for entity in entities:
            components = tuple(self._component_storage[c].get(entity) for c in component_types)
            yield entity, components

    def register_temporary_component(self, component_type: type[Component]) -> None:
        self._temporary_components.append(component_type)

    def get_temporary_components(self) -> list[type[Component]]:
        return self._temporary_components


class SystemManager:

    def __init__(self):
        self._systems: dict[ExecutionStage, list[System]] = defaultdict(list)
   
    @property
    def all_systems(self) -> Iterable[System]:
        return chain(*self._systems.values())

    def add(self, system: System, stage: ExecutionStage) -> None:
        if any(isinstance(s, type(system)) for s in self.all_systems):
            raise ValueError(f'System {type(system).__name__} already registered')
        self._systems[stage].append(system)

    def remove(self, system_type: type[System]) -> None:
        for stage, systems in self._systems.items():
            self._systems[stage] = [system for system in systems if not isinstance(system, system_type)]

    def execute(self, delta_time: float) -> None:
        for stage in ExecutionStage:
            for system in self._systems[stage]:
                system.execute(delta_time)


class ResourceManager:

    def __init__(self):
        self._resources: dict[type[Resource], Resource] = {}
   
    def set(self, resource: Resource) -> None:
        self._resources[type(resource)] = resource

    def get(self, resource_type: type[R]) -> R | None:
        return self._resources.get(resource_type, None)

    def remove(self, resource_type: type[Resource]) -> None:
        self._resources.pop(resource_type, None)


class EventManager:

    def __init__(self):
        self._events: list[Event] = []

    def push(self, event: Event) -> None:
        self._events.append(event)

    def get(self) -> list[Event]:
        return self._events
    
    def clear(self) -> None:
        self._events.clear()



class RenderManager:

    def __init__(self):
        self._queue: list[DrawCommandProtocol] = []

    def push(self, command: DrawCommandProtocol) -> None:
        self._queue.append(command)

    def get(self) -> list[DrawCommandProtocol]:
        return sorted(self._queue, key=lambda c: c.layer)
    
    def clear(self) -> None:
        self._queue.clear()
