from dataclasses import dataclass
from enum import Enum

from ecs_framework.types import Component
from core.primitives import Vec2


@dataclass(slots=True)
class Parent(Component):
    entity: int


@dataclass(slots=True)
class Children(Component):
    entities: set[int]


@dataclass(slots=True)
class Transform(Component):
    position: Vec2
    size: Vec2


@dataclass(slots=True)
class WorldTransform(Component):
    position: Vec2
    size: Vec2


@dataclass(slots=True)
class RenderLayer(Component):
    layer: int


@dataclass(slots=True)
class Padding(Component):
    left: int = 0
    right: int = 0
    top: int = 0
    bottom: int = 0


@dataclass(slots=True)
class Layout(Component): ...


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
class Anchor(Component):
    value: Vec2


class TextAlignmentEnum(Enum):
    left = 0
    center = 1
    right = 2


@dataclass(slots=True)
class TextAlignment(Component):
    alignment: TextAlignmentEnum
