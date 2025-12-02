import pygame
from ecs_architecture.component.sprites.board import UnitBoardSprite
from services.assets.core import AssetServiceConfig
from services.assets.service import AssetServiceFactory
from services.data.core import DataServiceConfig, DataType
from services.data.manager import DataManagerFactory
from services.data.service import DataService
from services.world.core import WorldServiceConfig
from services.world.service import WorldServiceFactory
from utils.config_loader import ConfigLoader
from utils.loader import YamlLoader


def test_entire_pipeline():
    config_loader = ConfigLoader(YamlLoader)
    data_service_config = config_loader.load_config(r'configuration\data_service.yaml', DataServiceConfig)
    asset_service_config = config_loader.load_config(r'configuration\asset_service.yaml', AssetServiceConfig)
    world_service_config = config_loader.load_config(r'configuration\world_service.yaml', WorldServiceConfig)

    data_service = DataService()
    for manager_config in data_service_config.data_managers:
        manager = DataManagerFactory.build(manager_config)
        data_service.register(manager_config.type, manager)
    data_service.load_all()

    pygame.init()
    pygame.display.set_mode()
    asset_service = AssetServiceFactory.build(asset_service_config)
    asset_service.scan()
    asset_service.load_all()

    world_service = WorldServiceFactory.build(world_service_config)
    
    unit = data_service.get(DataType.UNIT, 'Scout')

    world_name = 'world'
    world_service.build_world(world_name)
    entity = world_service.build_entity(world_name, unit)

    world = world_service.get_world(world_name)
    sprite_board: UnitBoardSprite = world.get_entity_component(entity, UnitBoardSprite)

    asset = asset_service.get(sprite_board.path)
    assert isinstance(asset, pygame.Surface)
    