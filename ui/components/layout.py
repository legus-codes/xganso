from dataclasses import dataclass

import pygame

from ecs_framework.ecs import ComponentProtocol


@dataclass
class Widget(ComponentProtocol):
    pass


@dataclass
class Parent(ComponentProtocol):
    entity: int


@dataclass
class RelativeRect(ComponentProtocol):
    rectangle: pygame.Rect


@dataclass
class Rect(ComponentProtocol):
    rectangle: pygame.Rect


@dataclass
class RectDirty(ComponentProtocol):
    pass
