from pygame import Surface

from omniecs.types import Component


class Sprite(Component):
    sprite: Surface


class ScreenSprite(Component):
    sprite: Surface
