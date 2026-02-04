from enum import Enum

from ecs_framework.ecs import ComponentProtocol
from ui.primitives import Vec2


class Parent(ComponentProtocol):
    entity: int


class Transform(ComponentProtocol):
    position: Vec2
    size: Vec2


class WorldTransform(ComponentProtocol):
    position: Vec2
    size: Vec2


class RenderLayer(ComponentProtocol):
    layer: int


class Padding(ComponentProtocol):
    left: int = 0
    right: int = 0
    top: int = 0
    bottom: int = 0


class Anchor(ComponentProtocol):
    value: Vec2


class AlignmentEnum(Enum):
    left = 0
    center = 1
    right = 2


class TextAlignment(ComponentProtocol):
    alignment: AlignmentEnum
