from typing import List, Protocol
import pygame

from ui.widgets import Widget


class Panel(Protocol):

    def __init__(self, screen: pygame.Surface, area: pygame.Rect, background: pygame.Color, frame_color: pygame.Color):
        self.screen = screen
        self.area = area
        self.background = background
        self.frame_color = frame_color
        self.surface = pygame.Surface(self.area.size, pygame.SRCALPHA)
        self.widgets: List[Widget] = []

    def add_widget(self, widget: Widget) -> None:
        self.widgets.append(widget)

    def handle_event(self, event: pygame.event.Event) -> None:
        adjusted_event = pygame.event.Event(event.type, **event.dict)
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
            relative_position = pygame.Vector2(event.pos) - pygame.Vector2(self.area.topleft)
            adjusted_event.pos = relative_position

        for widget in self.widgets:
            widget.handle_event(adjusted_event)

    def draw(self) -> None:
        self.surface.fill(self.background)
        for widget in self.widgets:
            widget.draw()
        pygame.draw.rect(self.surface, self.frame_color, self.surface.get_rect(), 2)
        self.screen.blit(self.surface, self.area.topleft)
