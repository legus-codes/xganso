import pygame
import pytest
from pathlib import Path
from typing import Any, Dict, List
from services.assets.service import AssetService
from utils.file_system import FileSystemProtocol
from utils.loader import LoaderProtocol


class MockLoader(LoaderProtocol):

    def __init__(self, data: Dict[Path, Any]):
        self.data = data

    def load_file(self, filepath: Path) -> Any:
        return self.data.get(filepath, None)


class MockFileSystem(FileSystemProtocol):
    
    def __init__(self, data: List[str]):
        self.data = data
    
    def glob(self, base_path: Path, pattern: str) -> List[Path]:
        return self.data


@pytest.fixture
def asset_service() -> AssetService:
    images = {
        Path('assets/unit/board.png'): 'BOARD',
        Path('assets/unit/character.png'): 'CHARACTER'
    }
    paths = [
        Path('assets/unit/board.png'),
        Path('assets/unit/character.png'),
    ]
    asset_service = AssetService(MockLoader(images), MockFileSystem(paths), 'assets')
    return asset_service

@pytest.fixture
def asset_service_with_error() -> AssetService:
    images = {
        Path('assets/unit/board.png'): 'BOARD',
        Path('assets/unit/character.png'): 'CHARACTER'
    }
    paths = [
        Path('unit/board.png'),
        Path('unit/character.png'),
    ]
    asset_service = AssetService(MockLoader(images), MockFileSystem(paths), 'assets')
    return asset_service

@pytest.fixture
def asset_paths() -> Dict[str, Path]:
    return {
        'unit/board': Path('assets/unit/board.png'),
        'unit/character': Path('assets/unit/character.png')
    }

@pytest.fixture
def assets() -> Dict[str, str]:
    return {
        'unit/board': 'BOARD',
        'unit/character': 'CHARACTER'
    }


def test_scan(asset_service: AssetService, asset_paths: Dict[str, Path]):    
    errors = asset_service.scan()
    assert errors == []
    assert asset_service.asset_paths == asset_paths
    assert asset_service.assets == {}

def test_scan_not_in_the_path(asset_service_with_error: AssetService):    
    errors = asset_service_with_error.scan()
    assert len(errors) == 2
    assert errors[0].filename == 'unit/board.png'
    assert "not in the subpath of 'assets'" in errors[0].message
    assert errors[1].filename == 'unit/character.png'
    assert "not in the subpath of 'assets'" in errors[1].message
    assert asset_service_with_error.asset_paths == {}
    assert asset_service_with_error.assets == {}

def test_load_all(asset_service: AssetService, asset_paths: Dict[str, Path], assets: Dict[str, str]):
    asset_service.scan()
    pygame.init()
    pygame.display.set_mode()
    asset_service.load_all()
    assert asset_service.asset_paths == asset_paths
    assert asset_service.assets == assets

def test_load_all_before_scan(asset_service: AssetService):
    asset_service.load_all()
    assert asset_service.asset_paths == {}
    assert asset_service.assets == {}

def test_reload_all(asset_service: AssetService):
    asset_service.scan()
    pygame.init()
    pygame.display.set_mode()
    asset_service.load_all()

    images = {
        Path('assets/item/small.png'): 'SMALL',
        Path('assets/item/large.png'): 'LARGE'
    }
    paths = [
        Path('assets/item/small.png'),
        Path('assets/item/large.png'),
    ]
    asset_paths = {
        'item/small': Path('assets/item/small.png'),
        'item/large': Path('assets/item/large.png')
    }
    assets = {
        'item/small': 'SMALL',
        'item/large': 'LARGE'
    }
    asset_service.loader = MockLoader(images)
    asset_service.file_provider = MockFileSystem(paths)
    errors = asset_service.reload_all()
    assert errors == []
    assert asset_service.asset_paths == asset_paths
    assert asset_service.assets == assets

def test_reload_all_with_errors(asset_service: AssetService):
    asset_service.scan()
    pygame.init()
    pygame.display.set_mode()
    asset_service.load_all()

    images = {
        Path('assets/item/small.png'): 'SMALL',
        Path('assets/item/large.png'): 'LARGE'
    }
    paths = [
        Path('assets/item/small.png'),
        Path('item/large.png'),
    ]
    asset_paths = {
        'item/small': Path('assets/item/small.png'),
        'item/large': Path('assets/item/large.png')
    }
    assets = {
        'item/small': 'SMALL',
        'item/large': 'LARGE'
    }
    asset_service.loader = MockLoader(images)
    asset_service.file_provider = MockFileSystem(paths)
    errors = asset_service.reload_all()
    assert len(errors) == 1
    assert errors[0].filename == 'item/large.png'
    assert "not in the subpath of 'assets'" in errors[0].message
    assert asset_service.asset_paths == {}
    assert asset_service.assets == {}

def test_get_existing_asset(asset_service: AssetService):
    asset_service.scan()
    pygame.init()
    pygame.display.set_mode()
    asset_service.load_all()
    asset = asset_service.get('unit/board')
    assert asset is not None
    assert asset == 'BOARD'

def test_get_non_existing_asset(asset_service: AssetService):
    asset_service: AssetService
    asset = asset_service.get('unit/board')
    assert asset is None

def test_get_keys(asset_service: AssetService):
    expected_keys = ['unit/board', 'unit/character']
    asset_service.scan()
    pygame.init()
    pygame.display.set_mode()
    asset_service.load_all()
    keys = asset_service.get_keys()
    assert keys == expected_keys

def test_get_identifier(asset_service: AssetService):
    identifier = asset_service._get_identifier(Path('assets/unit/board'))
    assert identifier == 'unit/board'

def test_get_identifier_not_in_the_path(asset_service: AssetService):
    with pytest.raises(ValueError):
        asset_service._get_identifier(Path('unit/board'))    
