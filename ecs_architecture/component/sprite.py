from dataclasses import dataclass
import pygame

from ecs_framework.ecs import ComponentProtocol


@dataclass
class Sprite(ComponentProtocol):
    sprite: pygame.Surface
