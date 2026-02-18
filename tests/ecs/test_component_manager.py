from ecs_framework.managers import ComponentManager, ComponentStorage
from ecs_framework.types import Component, EntityId


class MockComponent(Component): ...

class MockComponentA(Component): ...
class MockComponentB(Component): ...
class MockComponentC(Component): ...
class MockComponentD(Component): ...
class MockComponentE(Component): ...


def test_add_component_storage():
    component_storage = ComponentStorage[MockComponent]()
    entity_id = EntityId(1)
    component = MockComponent()
    component_storage.add(entity_id, component)

    assert component_storage.has(entity_id)
    assert component_storage.get(entity_id) == component

def test_remove_component_storage():
    component_storage = ComponentStorage[MockComponent]()
    entity_id = EntityId(1)
    component = MockComponent()
    component_storage.add(entity_id, component)
    component_storage.remove(entity_id)

    assert not component_storage.has(entity_id)
    assert component_storage.get(entity_id) is None

def test_remove_non_existing_entity():
    component_storage = ComponentStorage[MockComponent]()
    entity_id = EntityId(1)
    component_storage.remove(entity_id)

    assert not component_storage.has(entity_id)
    assert component_storage.get(entity_id) is None

def test_component_storage_entities():
    component_storage = ComponentStorage[MockComponent]()
    entity_ids = set([EntityId(1), EntityId(2), EntityId(3), EntityId(4)])
    component = MockComponent()
    for entity_id in entity_ids:
        component_storage.add(entity_id, component)

    assert component_storage.entities() == entity_ids

def test_add_component_manager():
    component_manager = ComponentManager()
    entity_id = EntityId(1)
    component_manager.add(entity_id, MockComponentA())

    assert component_manager.has(entity_id, MockComponentA)

def test_add_multiple_components_component_manager():
    component_manager = ComponentManager()
    entity_id = EntityId(1)
    component_manager.add(entity_id, MockComponentA())
    component_manager.add(entity_id, MockComponentB())
    component_manager.add(entity_id, MockComponentC())
    component_manager.add(entity_id, MockComponentD())

    assert component_manager.has(entity_id, MockComponentA)
    assert component_manager.has(entity_id, MockComponentB)
    assert component_manager.has(entity_id, MockComponentC)
    assert component_manager.has(entity_id, MockComponentD)

def test_remove_component_manager():
    component_manager = ComponentManager()
    entity_id = EntityId(1)
    component_manager.add(entity_id, MockComponentA())
    component_manager.remove(entity_id, MockComponentA)

    assert not component_manager.has(entity_id, MockComponentA)

def test_destroy_component_manager():
    component_manager = ComponentManager()
    entity_id = EntityId(1)
    component_manager.add(entity_id, MockComponentA())
    component_manager.add(entity_id, MockComponentB())
    component_manager.add(entity_id, MockComponentC())
    component_manager.add(entity_id, MockComponentD())
    component_manager.destroy(entity_id)

    assert not component_manager.has(entity_id, MockComponentA)
    assert not component_manager.has(entity_id, MockComponentB)
    assert not component_manager.has(entity_id, MockComponentC)
    assert not component_manager.has(entity_id, MockComponentD)

def test_query_all_of_entities_component_manager():
    component_manager = ComponentManager()
    entity_id1 = EntityId(1)
    entity_id2 = EntityId(2)
    entity_id3 = EntityId(3)
    entity_id4 = EntityId(4)
    entity_id5 = EntityId(5)
    component_manager.add(entity_id1, MockComponentA())
    component_manager.add(entity_id2, MockComponentB())
    component_manager.add(entity_id3, MockComponentC())
    component_manager.add(entity_id4, MockComponentD())
    component_manager.add(entity_id5, MockComponentE())
    component_manager.add(entity_id2, MockComponentE())
    
    entities = component_manager.query_entities(all_of=(MockComponentB, MockComponentE))
    assert entities == set([entity_id2])

def test_query_any_of_entities_component_manager():
    component_manager = ComponentManager()
    entity_id1 = EntityId(1)
    entity_id2 = EntityId(2)
    entity_id3 = EntityId(3)
    entity_id4 = EntityId(4)
    entity_id5 = EntityId(5)
    component_manager.add(entity_id1, MockComponentA())
    component_manager.add(entity_id2, MockComponentB())
    component_manager.add(entity_id3, MockComponentC())
    component_manager.add(entity_id4, MockComponentD())
    component_manager.add(entity_id5, MockComponentE())
    component_manager.add(entity_id3, MockComponentA())
    
    entities = component_manager.query_entities(any_of=(MockComponentA, MockComponentD))
    assert entities == set([entity_id1, entity_id3, entity_id4])

def test_query_none_of_entities_component_manager():
    component_manager = ComponentManager()
    entity_id1 = EntityId(1)
    entity_id2 = EntityId(2)
    entity_id3 = EntityId(3)
    entity_id4 = EntityId(4)
    entity_id5 = EntityId(5)
    component_manager.add(entity_id1, MockComponentA())
    component_manager.add(entity_id2, MockComponentB())
    component_manager.add(entity_id3, MockComponentC())
    component_manager.add(entity_id4, MockComponentD())
    component_manager.add(entity_id5, MockComponentE())
    component_manager.add(entity_id1, MockComponentB())
    
    entities = component_manager.query_entities(none_of=(MockComponentB, MockComponentC))
    assert entities == set([entity_id4, entity_id5])

def test_query_entities_component_manager():
    component_manager = ComponentManager()
    entity_id1 = EntityId(1)
    entity_id2 = EntityId(2)
    entity_id3 = EntityId(3)
    entity_id4 = EntityId(4)
    entity_id5 = EntityId(5)
    component_manager.add(entity_id1, MockComponentA())
    component_manager.add(entity_id1, MockComponentB())
    component_manager.add(entity_id1, MockComponentC())
    component_manager.add(entity_id2, MockComponentB())
    component_manager.add(entity_id2, MockComponentD())
    component_manager.add(entity_id3, MockComponentC())
    component_manager.add(entity_id3, MockComponentE())
    component_manager.add(entity_id4, MockComponentB())
    component_manager.add(entity_id4, MockComponentE())
    component_manager.add(entity_id5, MockComponentA())
    component_manager.add(entity_id5, MockComponentE())
    
    entities = component_manager.query_entities(all_of=(MockComponentB,), any_of=(MockComponentA, MockComponentD), none_of=(MockComponentE,))
    assert entities == set([entity_id1, entity_id2])

def test_query_component_manager():
    component_manager = ComponentManager()
    entity_id1 = EntityId(1)
    entity_id2 = EntityId(2)
    entity_id3 = EntityId(3)
    entity_id4 = EntityId(4)
    entity_id5 = EntityId(5)
    component = MockComponentC()
    component_manager.add(entity_id1, MockComponentA())
    component_manager.add(entity_id1, MockComponentB())
    component_manager.add(entity_id1, component)
    component_manager.add(entity_id2, MockComponentB())
    component_manager.add(entity_id2, MockComponentD())
    component_manager.add(entity_id3, MockComponentC())
    component_manager.add(entity_id3, MockComponentE())
    component_manager.add(entity_id4, MockComponentB())
    component_manager.add(entity_id4, MockComponentE())
    component_manager.add(entity_id5, MockComponentA())
    component_manager.add(entity_id5, MockComponentE())
    
    entities = list(component_manager.query(MockComponentC, all_of=(MockComponentB,), any_of=(MockComponentA, MockComponentD), none_of=(MockComponentE,)))
    assert len(entities) == 1
    entity, (queried_component,) = entities[0]
    assert entity == entity_id1
    assert queried_component == component
