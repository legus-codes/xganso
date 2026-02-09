from collections import defaultdict
from typing import Any, Iterable, TypeVarTuple

from ecs_framework.managers.entity_manager import EntityId
from ecs_framework.primitives import ComponentProtocol

Cs = TypeVarTuple("Cs")


class ComponentStorage[C: ComponentProtocol]:

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
        self._world: dict[type[ComponentProtocol], ComponentStorage[Any]] = defaultdict(ComponentStorage)

    def add(self, entity_id: EntityId, component: ComponentProtocol) -> None:
        self._world[type(component)].add(entity_id, component)

    def remove(self, entity_id: EntityId, component_type: type[ComponentProtocol]) -> None:
        self._world.get(component_type, ComponentStorage()).remove(entity_id)

    def destroy(self, entity_id: EntityId) -> None:
        for storage in self._world.values():
            storage.remove(entity_id)

    def has(self, entity_id: EntityId, component_type: type[ComponentProtocol]) -> bool:
        return component_type in self._world and self._world[component_type].has(entity_id)

    def query_entities(self,
                       all_of: tuple[type[ComponentProtocol], ...] = (),
                       any_of: tuple[type[ComponentProtocol], ...] = (),
                       none_of: tuple[type[ComponentProtocol], ...] = ()
     ) -> set[EntityId]:
        
        entities = set.union(*(storage.entities() for storage in self._world.values()))

        if all_of:
            for component in all_of:
                entities.intersection_update(self._world[component].entities())
            if not entities:
                return entities

        if any_of:
            candidates = set.union(*(self._world[c].entities() for c in any_of if c in self._world))
            entities.intersection_update(candidates)
            if not entities:
                return entities

        if none_of:
            candidates = set.union(*(self._world[c].entities() for c in none_of if c in self._world))
            entities.difference_update(candidates)

        return entities

    def query(self,
              *component_types: *Cs,
              all_of: tuple[type[ComponentProtocol], ...] = (),
              any_of: tuple[type[ComponentProtocol], ...] = (),
              none_of: tuple[type[ComponentProtocol], ...] = ()
     ) -> Iterable[tuple[EntityId, tuple[*Cs]]]:
        entities = self.query_entities(all_of + component_types, any_of, none_of)

        for entity in entities:
            components = tuple(self._world[c].get(entity) for c in component_types)
            yield entity, components

    def clear(self) -> None:
        self._world.clear()
