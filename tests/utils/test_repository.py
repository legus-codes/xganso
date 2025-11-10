from pathlib import Path
from utils.repository import YamlRepository


def test_load_all_correctly_yaml_data():
    yaml_repository = YamlRepository()
    data = yaml_repository.load_all(Path('tests/utils/data'))
    assert isinstance(data, dict)
    assert len(data) > 0


def test_load_file_correctly_yaml_data():
    yaml_repository = YamlRepository()
    data = yaml_repository.load_file(Path('tests/utils/data/test.yaml'))
    assert isinstance(data, dict)
    assert len(data) > 0
