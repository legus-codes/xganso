from dataclasses import dataclass
from typing import Callable

import pygame

from ecs_framework.ecs import ComponentProtocol


@dataclass
class UIElement(ComponentProtocol):
    pass


@dataclass
class UILabel(ComponentProtocol):
    label: str


@dataclass
class UIRect(ComponentProtocol):
    rectangle: pygame.Rect


@dataclass
class UIColor(ComponentProtocol):
    text: pygame.Color
    background: pygame.Color
    hover: pygame.Color
    press: pygame.Color
    select: pygame.Color


@dataclass
class UIFont(ComponentProtocol):
    font: pygame.font.Font


@dataclass
class UIState(ComponentProtocol):
    enabled: bool
    focused: bool = False
    hovered: bool = False
    pressed: bool = False
    selected: bool = False


@dataclass
class UIPadding(ComponentProtocol):
    left: int = 0
    right: int = 0
    top: int = 0
    bottom: int = 0


@dataclass
class UIText(ComponentProtocol):
    text: str


@dataclass
class UICallback(ComponentProtocol):
    callback: Callable


@dataclass
class UIString(ComponentProtocol):
    variable: str


@dataclass
class UIInt(ComponentProtocol):
    variable: int


