from collections import defaultdict
from typing import Any, Iterable

from ecs_framework.managers.entity_manager import EntityId
from ecs_framework.primitives import ComponentProtocol
from ecs_framework.protocols import ComponentManagerProtocol, Cs


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


class ComponentManager(ComponentManagerProtocol):

    def __init__(self):
        self._component_storage: dict[type[ComponentProtocol], ComponentStorage[Any]] = defaultdict(ComponentStorage)
        self._temporary_components: list[type[ComponentProtocol]] = []

    def add(self, entity_id: EntityId, component: ComponentProtocol) -> None:
        self._component_storage[type(component)].add(entity_id, component)

    def remove(self, entity_id: EntityId, component_type: type[ComponentProtocol]) -> None:
        self._component_storage.get(component_type, ComponentStorage()).remove(entity_id)

    def remove_all(self, component_type: type[ComponentProtocol]) -> None:
        self._component_storage.pop(component_type, None)

    def destroy(self, entity_id: EntityId) -> None:
        for storage in self._component_storage.values():
            storage.remove(entity_id)

    def has(self, entity_id: EntityId, component_type: type[ComponentProtocol]) -> bool:
        return component_type in self._component_storage and self._component_storage[component_type].has(entity_id)

    def query_entities(self,
                       all_of: tuple[type[ComponentProtocol], ...] = (),
                       any_of: tuple[type[ComponentProtocol], ...] = (),
                       none_of: tuple[type[ComponentProtocol], ...] = ()
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
              all_of: tuple[type[ComponentProtocol], ...] = (),
              any_of: tuple[type[ComponentProtocol], ...] = (),
              none_of: tuple[type[ComponentProtocol], ...] = ()
     ) -> Iterable[tuple[EntityId, tuple[*Cs]]]:
        entities = self.query_entities(all_of + component_types, any_of, none_of)

        for entity in entities:
            components = tuple(self._component_storage[c].get(entity) for c in component_types)
            yield entity, components

    def register_temporary_component(self, component_type: type[ComponentProtocol]) -> None:
        self._temporary_components.append(component_type)

    def get_temporary_components(self) -> list[type[ComponentProtocol]]:
        return self._temporary_components

    def clear(self) -> None:
        self._component_storage.clear()
        self._temporary_components.clear()
