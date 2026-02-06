from dataclasses import dataclass
from enum import Enum
from typing import Set

from ecs_framework.ecs import ComponentProtocol
from ui.primitives import Vec2


@dataclass(slots=True)
class Parent(ComponentProtocol):
    entity: int


@dataclass(slots=True)
class Children(ComponentProtocol):
    entities: Set[int]


@dataclass(slots=True)
class Transform(ComponentProtocol):
    position: Vec2
    size: Vec2


@dataclass(slots=True)
class WorldTransform(ComponentProtocol):
    position: Vec2
    size: Vec2


@dataclass(slots=True)
class RenderLayer(ComponentProtocol):
    layer: int


@dataclass(slots=True)
class Padding(ComponentProtocol):
    left: int = 0
    right: int = 0
    top: int = 0
    bottom: int = 0


@dataclass(slots=True)
class Layout(ComponentProtocol): ...


@dataclass(slots=True)
class HorizontalLayout(Layout):
    spacing: int


@dataclass(slots=True)
class VerticalLayout(Layout):
    spacing: int


@dataclass(slots=True)
class GridLayout(Layout):
    rows: int
    cols: int
    h_spacing: int
    v_spacing: int


@dataclass(slots=True)
class Anchor(ComponentProtocol):
    value: Vec2


class TextAlignmentEnum(Enum):
    left = 0
    center = 1
    right = 2


@dataclass(slots=True)
class TextAlignment(ComponentProtocol):
    alignment: TextAlignmentEnum
