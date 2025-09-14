from dataclasses import dataclass
from enum import Enum

import pygame

from ecs_framework.ecs import ComponentProtocol


class Allignment(Enum):
    left = 0
    center = 1
    right = 2


@dataclass
class Color(ComponentProtocol):
    text: pygame.Color
    background: pygame.Color
    hover: pygame.Color
    press: pygame.Color
    focus: pygame.Color
    select: pygame.Color
    frame: pygame.Color


@dataclass
class Font(ComponentProtocol):
    font: pygame.font.Font


@dataclass
class Padding(ComponentProtocol):
    left: int = 0
    right: int = 0
    top: int = 0
    bottom: int = 0


@dataclass
class TextAllignment(ComponentProtocol):
    allignment: Allignment
