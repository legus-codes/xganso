from services.world.core import WorldServiceConfig
from services.world.service import WorldServiceFactory
from utils.config_loader import ConfigLoader
from utils.loader import YamlLoader


def test_start_world_service():
    config_loader = ConfigLoader(YamlLoader)
    world_service_config = config_loader.load_config(r'configuration\world_service.yaml', WorldServiceConfig)

    world_service = WorldServiceFactory.build(world_service_config)
