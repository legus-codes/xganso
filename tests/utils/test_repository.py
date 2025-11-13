import pygame

from pathlib import Path
from utils.loader import PngLoader, YamlLoader


def test_load_yaml_file_correctly():
    yaml_loader = YamlLoader()
    data = yaml_loader.load_file(Path('tests/utils/data/test.yaml'))
    assert isinstance(data, dict)
    assert len(data) > 0

def test_load_png_file_correctly():
    pygame.init()
    pygame.display.set_mode()
    png_loader = PngLoader()
    data = png_loader.load_file(Path('tests/utils/data/ganso-board.png'))
    assert isinstance(data, pygame.Surface)
    pygame.quit()

def test_load_png_file_fails_display_not_initialized():
    png_loader = PngLoader()
    data = png_loader.load_file(Path('tests/utils/data/ganso-board.png'))
    assert data is None
