from services.assets.core import AssetServiceConfig
from services.assets.service import AssetServiceFactory
from utils.config_loader import ConfigLoader
from utils.loader import YamlLoader


def test_start_asset_service():
    config_loader = ConfigLoader(YamlLoader)
    asset_service_config = config_loader.load_config(r'configuration\asset_service.yaml', AssetServiceConfig)

    asset_service = AssetServiceFactory.build(asset_service_config)
    errors = asset_service.scan()
    assert errors == []
