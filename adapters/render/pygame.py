import pygame

from adapters.render.commands import DrawFrame, DrawInput, DrawRectangle, DrawText
from omniecs.types import DrawCommand

from core.primitives import IVec2
from ui.components.layout import HorizontalAlignment, VerticalAlignment


class PygameRenderer:
    
    def __init__(self, screen: pygame.Surface):
        self.screen = screen

    def render(self, draw_commands: list[DrawCommand]) -> None:
        for draw_command in sorted(draw_commands, key=lambda command: (command.global_layer, command.local_layer)):
            self.draw(draw_command)

        self.screen.blit(self.screen, (0, 0))

    def draw(self, draw_command: DrawCommand) -> None:
        match draw_command:
            case DrawInput():
                draw_command: DrawInput
                color = pygame.Color(*draw_command.color.tuple)
                font = pygame.font.SysFont(draw_command.font_id, draw_command.font_size)
                surface = font.render(draw_command.text + draw_command.value, True, color)
                spacing = draw_command.spacing
                offset = self._get_text_offset(draw_command.size, IVec2(*surface.get_size()), draw_command.horizontal_alignment, draw_command.vertical_alignment)
                position = draw_command.position + offset + spacing
                self.screen.blit(surface, position.tuple)

            case DrawText():
                draw_command: DrawText
                color = pygame.Color(*draw_command.color.tuple)
                font = pygame.font.SysFont(draw_command.font_id, draw_command.font_size)
                surface = font.render(draw_command.text, True, color)
                spacing = draw_command.spacing
                offset = self._get_text_offset(draw_command.size, IVec2(*surface.get_size()), draw_command.horizontal_alignment, draw_command.vertical_alignment)
                position = draw_command.position + offset + spacing
                self.screen.blit(surface, position.tuple)

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

    def _get_text_offset(self, area_size: IVec2, text_size: IVec2, horizontal_alignment: HorizontalAlignment, vertical_alignment: VerticalAlignment) -> IVec2:
        match horizontal_alignment:
            case HorizontalAlignment.left:
                x = 0
            case HorizontalAlignment.center:
                x = (area_size.x - text_size.x) / 2
            case HorizontalAlignment.right:
                x = area_size.x - text_size.x

        match vertical_alignment:
            case VerticalAlignment.top:
                y = 0
            case VerticalAlignment.middle:
                y = (area_size.y - text_size.y) / 2
            case VerticalAlignment.bottom:
                y = area_size.y - text_size.y

        return IVec2(x, y)
