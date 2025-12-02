from typing import Any, Dict, List
from ecs_architecture.component.builder import ComponentBuilderProtocol
from ecs_architecture.component.identity.identifier import Identifier
from ecs_framework.ecs import ECS, ComponentProtocol
from services.data.models import DataDescription, IdentityDataDescription
from services.world.service import WorldService


class MockComponentBuilder(ComponentBuilderProtocol):

    def build(self, data: Dict[str, Dict[str, Any]]) -> List[ComponentProtocol]:
        return [Identifier(identity=data['identity']['id'])]

def create_data_description(identifier: str) -> DataDescription:
    identity = IdentityDataDescription(id=identifier)
    return DataDescription(identity=identity)


def test_create_world_service_with_no_worlds():
    world_service = WorldService(MockComponentBuilder())
    assert world_service.worlds == {}

def test_build_world():
    world_service = WorldService(MockComponentBuilder())
    world_service.build_world('test')
    assert world_service.has_world('test')
    
def test_build_existing_world():
    world_service = WorldService(MockComponentBuilder())
    world_service.build_world('test')
    world = world_service.get_world('test')
    world_service.build_world('test')
    world2 = world_service.get_world('test')
    assert world == world2

def test_has_non_existing_world():
    world_service = WorldService(MockComponentBuilder())
    assert not world_service.has_world('test')

def test_get_world():
    world_service = WorldService(MockComponentBuilder())
    world_service.build_world('test')
    world = world_service.get_world('test')
    assert isinstance(world, ECS)

def test_get_non_existing_world():
    world_service = WorldService(MockComponentBuilder())
    world = world_service.get_world('test')
    assert world is None

def test_destroy_world():
    world_service = WorldService(MockComponentBuilder())
    world_service.build_world('test')
    world_service.destroy_world('test')
    assert not world_service.has_world('test')

def test_destroy_non_existing_world():
    world_service = WorldService(MockComponentBuilder())
    world_service.build_world('test')
    world_service.destroy_world('test2')
    assert world_service.has_world('test')

def test_build_entity():
    world_service = WorldService(MockComponentBuilder())
    world_service.build_world('test')
    data = create_data_description('data')
    entity = world_service.build_entity('test', data)
    world = world_service.get_world('test')
    assert isinstance(entity, int)
    assert world.has_entity(entity)
    assert world.entity_has_component(entity, Identifier)

def test_build_entity_non_existing_world():
    world_service = WorldService(MockComponentBuilder())
    data = create_data_description('data')
    entity = world_service.build_entity('test', data)
    assert entity is None

def test_delete_entity():
    world_service = WorldService(MockComponentBuilder())
    world_service.build_world('test')
    data = create_data_description('data')
    entity = world_service.build_entity('test', data)
    world_service.destroy_entity('test', entity)
    world = world_service.get_world('test')
    assert not world.has_entity(entity)
    assert not world.entity_has_component(entity, Identifier)

def test_delete_entity_non_existing_world():
    world_service = WorldService(MockComponentBuilder())
    world_service.destroy_entity('test', 0)

def test_delete_entity_non_existing_entity():
    world_service = WorldService(MockComponentBuilder())
    world_service.build_world('test')
    world_service.destroy_entity('test', 0)
