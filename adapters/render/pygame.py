import pygame

from adapters.render.commands import DrawFrame, DrawRectangle, DrawText
from omniecs.types import DrawCommand


class PygameRenderer:
    
    def __init__(self, screen: pygame.Surface):
        self.screen = screen

    def render(self, draw_commands: list[DrawCommand]) -> None:
        for draw_command in sorted(draw_commands, key=lambda command: (command.global_layer, command.local_layer)):
            self.draw(draw_command)

        self.screen.blit(self.screen, (0, 0))

    def draw(self, draw_command: DrawCommand) -> None:
        match draw_command:
            case DrawFrame():
                draw_command: DrawFrame
                color = pygame.Color(*draw_command.color.tuple)
                rect = pygame.Rect(*draw_command.position.tuple, *draw_command.size.tuple)
                pygame.draw.rect(self.screen, color, rect, draw_command.width)

            case DrawRectangle():
                draw_command: DrawRectangle
                color = pygame.Color(*draw_command.color.tuple)
                rect = pygame.Rect(*draw_command.position.tuple, *draw_command.size.tuple)
                pygame.draw.rect(self.screen, color, rect)

            case DrawText():
                ...
