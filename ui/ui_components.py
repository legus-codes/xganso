from dataclasses import dataclass
from enum import Enum
from typing import Callable, List

import pygame

from ecs_framework.ecs import ComponentProtocol


class Allignment(Enum):
    left = 0
    center = 1
    right = 2


@dataclass
class UIElement(ComponentProtocol):
    pass


@dataclass
class UILabel(ComponentProtocol):
    label: str
    allignment: Allignment


@dataclass
class UIParent(ComponentProtocol):
    entity: int


@dataclass
class UIRelativeRect(ComponentProtocol):
    rectangle: pygame.Rect


@dataclass
class UIRect(ComponentProtocol):
    rectangle: pygame.Rect


@dataclass
class UIRectDirty(ComponentProtocol):
    pass


@dataclass
class UIColor(ComponentProtocol):
    text: pygame.Color
    background: pygame.Color
    hover: pygame.Color
    press: pygame.Color
    focus: pygame.Color
    select: pygame.Color
    frame: pygame.Color


@dataclass
class UIFont(ComponentProtocol):
    font: pygame.font.Font


@dataclass
class UIPadding(ComponentProtocol):
    left: int = 0
    right: int = 0
    top: int = 0
    bottom: int = 0


@dataclass
class UIRadioGroup(ComponentProtocol):
    name: str


@dataclass
class UICallback(ComponentProtocol):
    callback: Callable


@dataclass
class UIVariable(ComponentProtocol):
    value: str
    variable_type: type


@dataclass
class UIRenderLayer(ComponentProtocol):
    layer: int


@dataclass
class UIEnabled(ComponentProtocol):
    pass


@dataclass
class UIHoverable(ComponentProtocol):
    pass


@dataclass
class UIHovered(ComponentProtocol):
    pass


@dataclass
class UIPressable(ComponentProtocol):
    pass


@dataclass
class UIPressed(ComponentProtocol):
    pass


@dataclass
class UIFocusable(ComponentProtocol):
    pass


@dataclass
class UIFocused(ComponentProtocol):
    pass


@dataclass
class UIToggleable(ComponentProtocol):
    pass


@dataclass
class UIToggled(ComponentProtocol):
    pass


@dataclass
class UISelectable(ComponentProtocol):
    pass


@dataclass
class UISelected(ComponentProtocol):
    pass


@dataclass
class UITypeable(ComponentProtocol):
    accepted_chars: List[str]


@dataclass
class UIFrameable(ComponentProtocol):
    pass


@dataclass
class UIForceRedraw(ComponentProtocol):
    pass


@dataclass
class UINeedRedraw(ComponentProtocol):
    pass


@dataclass
class UIRenderable(ComponentProtocol):
    pass


@dataclass
class UIHighlightable(ComponentProtocol):
    pass


@dataclass
class UILabelable(ComponentProtocol):
    pass


