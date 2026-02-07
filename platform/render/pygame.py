from typing import List
import pygame
from ecs_framework.ecs import DrawCommand
from platform.render.commands import DrawRect, DrawText


class PygameRenderer:
    
    def __init__(self, screen: pygame.Surface):
        self.screen = screen

    def render(self, draw_commands: List[DrawCommand]) -> None:
        for draw_command in sorted(draw_commands, key=lambda command: command.z):
            self.draw(draw_command)


    def draw(self, draw_command: DrawCommand) -> None:
        match DrawCommand:
            case DrawRect():
                pygame.draw.rect(...)

            case DrawText():
                ...
