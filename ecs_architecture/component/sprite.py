from pygame import Surface

from ecs_framework.ecs import ComponentProtocol


class Sprite(ComponentProtocol):
    sprite: Surface


class ScreenSprite(ComponentProtocol):
    sprite: Surface
