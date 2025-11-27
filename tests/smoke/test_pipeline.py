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
    data_service = DataService()
    for manager_config in data_service_config.data_managers:
        manager = DataManagerFactory.build(manager_config)
        data_service.register(manager_config.type, manager)
    data_service.load_all()
    
    unit_data = data_service.get(DataType.UNIT, 'Scout')
    assert unit_data is not None
