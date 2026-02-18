import pygame

from adapters.render.commands import DrawRect, DrawText
from ecs_framework.types import DrawCommandProtocol


class PygameRenderer:
    
    def __init__(self, screen: pygame.Surface):
        self.screen = screen

    def render(self, draw_commands: list[DrawCommandProtocol]) -> None:
        for draw_command in sorted(draw_commands, key=lambda command: command.z):
            self.draw(draw_command)


    def draw(self, draw_command: DrawCommandProtocol) -> None:
        match DrawCommandProtocol:
            case DrawRect():
                pygame.draw.rect(...)

            case DrawText():
                ...
