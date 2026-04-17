from dataclasses import dataclass, field
from enum import Enum

from omniecs.types import Component, EntityId
from core.primitives import Vec2


@dataclass(slots=True)
class Parent(Component):
    entity: EntityId


@dataclass(slots=True)
class Children(Component):
    entities: set[EntityId] = field(default_factory=set)  


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
class Spacing(Component):
    horizontal: int = 0
    vertical: int = 0


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


class HorizontalAlignment(Enum):
    left = 0
    center = 1
    right = 2


class VerticalAlignment(Enum):
    top = 0
    middle = 1
    bottom = 2


@dataclass(slots=True)
class TextAlignment(Component):
    horizontal: HorizontalAlignment
    vertical: VerticalAlignment
