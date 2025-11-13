from pathlib import Path
from typing import Any, Protocol

import pygame
import yaml


class LoaderProtocol(Protocol):

    @staticmethod
    def load_file(filepath: Path) -> Any:
        ...


class YamlLoader(LoaderProtocol):

    @staticmethod
    def load_file(filepath: Path) -> Any:
        with open(filepath) as yaml_file:
            return yaml.safe_load(yaml_file)


class PngLoader(LoaderProtocol):

    @staticmethod
    def load_file(filepath: Path) -> Any:
        try:
            return pygame.image.load(filepath).convert()
        except pygame.error:
            return None
