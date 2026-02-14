from itertools import count

from ecs_framework.primitives import EntityId
from ecs_framework.protocols import EntityManagerProtocol


class EntityManager(EntityManagerProtocol):

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

    def clear(self) -> None:
        self._entities.clear()
