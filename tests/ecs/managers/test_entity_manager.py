from ecs_framework.managers.entity_manager import EntityId, EntityManager


def test_create_entity():
    entity_manager = EntityManager()
    entity = entity_manager.create()
    assert entity_manager.exists(entity)
    assert isinstance(entity, EntityId)


def test_create_multiple_entities():
    entity_manager = EntityManager()
    entity1 = entity_manager.create()
    entity2 = entity_manager.create()
    assert entity1 != entity2


def test_destroy_entity():
    entity_manager = EntityManager()
    entity = entity_manager.create()
    entity_manager.destroy(entity)
    assert not entity_manager.exists(entity)


def test_destroy_non_existing_entity():
    entity_manager = EntityManager()
    entity = entity_manager.create()
    entity_manager.destroy(EntityId(12))
    assert entity_manager.exists(entity)


def test_clear_entities():
    entity_manager = EntityManager()
    entity_manager.create()
    entity_manager.create()
    entity_manager.clear()
    assert len(entity_manager._entities) == 0