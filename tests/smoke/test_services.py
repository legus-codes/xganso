from services.assets.core import AssetServiceConfig
from services.assets.service import AssetServiceFactory
from services.data.core import DataServiceConfig
from services.data.manager import DataManagerFactory
from services.data.service import DataService
from utils.config_loader import ConfigLoader
from utils.loader import YamlLoader


def test_start_data_service():
    config_loader = ConfigLoader(YamlLoader)
    data_service_config = config_loader.load_config(r'configuration\data_service.yaml', DataServiceConfig)
    data_service = DataService()
    for manager_config in data_service_config.data_managers:
        manager = DataManagerFactory.build(manager_config)
        data_service.register(manager_config.type, manager)
    errors = data_service.load_all()
    assert errors == []


def test_start_asset_service():
    config_loader = ConfigLoader(YamlLoader)
    asset_service_config = config_loader.load_config(r'configuration\asset_service.yaml', AssetServiceConfig)

    asset_service = AssetServiceFactory.build(asset_service_config)
    errors = asset_service.scan()
    assert errors == []

    # world_service_config = config_loader.load_config(r'configuration\world_service.yaml', AssetServiceConfig)