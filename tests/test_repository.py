from pathlib import Path
from utils.repository import YamlRepository


def test_load_correctly_yaml_data():
    yaml_repository = YamlRepository(Path('tests/data'))
    data = yaml_repository.load()
    assert isinstance(data, list)
    assert len(data) > 0
