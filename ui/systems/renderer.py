import pygame
from ecs_framework.ecs import ECS, SystemProtocol
from ui.components.data import Label, RenderLayer, Variable
from ui.components.formatting import Allignment, TextAllignment, Color, Font
from ui.components.layout import Widget, Parent, Rect, RelativeRect
from ui.components.rendering import ForceRedraw, Frameable, Highlightable, Labelable, NeedRedraw, Renderable
from ui.components.state import Enabled, Focused, Hovered, Pressed, Selected, Toggled


def _center_middle_position(rect: pygame.Rect, text_rect: pygame.Surface) -> pygame.Vector2:
    x = rect.left + (rect.width - text_rect.get_width()) / 2
    y = rect.top + (rect.height - text_rect.get_height()) / 2
    return pygame.Vector2(x, y)


def _left_middle_position(rect: pygame.Rect, text_rect: pygame.Surface) -> pygame.Vector2:
    x = rect.left + 5
    y = rect.top + (rect.height - text_rect.get_height()) / 2
    return pygame.Vector2(x, y)


class RelativeToRectConverter(SystemProtocol):

    def __init__(self, world: ECS):
        self.world = world

    def execute(self, delta_time: float):
        for entity, (parent, relative_rect, _, _) in self.world.get_entities_with_components(Parent, RelativeRect, Widget, Enabled):
            if self.world.entity_has_component(entity, Rect):
                continue

            if not self.world.entity_has_component(parent.entity, Rect):
                continue

            parent_rect: Rect = self.world.get_entity_component(parent.entity, Rect)
            rect = Rect(relative_rect.rectangle.move(parent_rect.rectangle.topleft))
            self.world.add_component(entity, rect)


class RendererSystem(SystemProtocol):

    def __init__(self, world: ECS, screen: pygame.Surface):
        self.world = world
        self.screen = screen

    def execute(self, delta_time: float):
        all_entities = []
        for entity in self.world.get_entities_with(Widget, Enabled, Renderable, Color, Rect):
            render_layer: RenderLayer = self.world.get_entity_component(entity, RenderLayer)
            layer = render_layer.layer if render_layer is not None else 100
            all_entities.append((entity, layer))

        all_entities.sort(key=lambda x: x[1])

        for entity, layer in all_entities:
            if not (self.world.entity_has_component(entity, ForceRedraw) or self.world.entity_has_component(entity, NeedRedraw)):
                continue

            rect: Rect = self.world.get_entity_component(entity, Rect)
            colors: Color = self.world.get_entity_component(entity, Color)
            self.screen.set_clip(rect.rectangle)
            
            self.draw_background(entity, rect, colors)
            if self.world.entity_has_component(entity, Highlightable):
                self.draw_highlight(entity, rect, colors)
            if self.world.entity_has_component(entity, Labelable):
                self.draw_text(entity, rect, colors)

            self.screen.set_clip(None)

    def draw_background(self, entity: int, rect: Rect, colors: Color) -> None:
        background = colors.background
        if self.world.entity_has_component(entity, Toggled):
            background = colors.select
        if self.world.entity_has_component(entity, Selected):
            background = colors.select
        if self.world.entity_has_component(entity, Pressed):
            background = colors.press

        pygame.draw.rect(self.screen, background, rect.rectangle)

    def draw_highlight(self, entity: int, rect: Rect, colors: Color) -> None:
        if self.world.entity_has_component(entity, Frameable):
            pygame.draw.rect(self.screen, colors.frame, rect.rectangle, 2)
        if self.world.entity_has_component(entity, Hovered):
            pygame.draw.rect(self.screen, colors.hover, rect.rectangle, 2)
        if self.world.entity_has_component(entity, Focused):
            pygame.draw.rect(self.screen, colors.focus, rect.rectangle, 2)

    def draw_text(self, entity: int, rect: Rect, colors: Color) -> None:
        if not self.world.entity_has_component(entity, Font):
            return

        font: Font = self.world.get_entity_component(entity, Font)
        label_width: pygame.Vector2 = (0, 0)

        if self.world.entity_has_component(entity, Label):
            label: Label = self.world.get_entity_component(entity, Label)
            allignment: TextAllignment = self.world.get_entity_component(entity, TextAllignment)

            label_surface = font.font.render(label.label, True, colors.text)
            label_position = _center_middle_position(rect.rectangle, label_surface)
            if allignment and allignment.allignment == Allignment.left:
                label_position = _left_middle_position(rect.rectangle, label_surface)
            label_width = pygame.Vector2(label_surface.get_width(), 0)
            self.screen.blit(label_surface, label_position)

        if self.world.entity_has_component(entity, Variable):
            variable: Variable = self.world.get_entity_component(entity, Variable)

            text_surface = font.font.render(variable.value, True, colors.text)
            text_position = _left_middle_position(rect.rectangle, text_surface) + label_width
            self.screen.blit(text_surface, text_position)

            if self.world.entity_has_component(entity, Focused):
                cursor_position = text_position.xy + pygame.Vector2(text_surface.get_width() + 2, 0)
                cursor_height = text_surface.get_height()
                pygame.draw.line(self.screen, colors.text, cursor_position, cursor_position + pygame.Vector2(0, cursor_height))


class CleanupRendererSystem(SystemProtocol):

    def __init__(self, world: ECS):
        self.world = world

    def execute(self, delta_time: float):
        for entity in self.world.get_entities_with(NeedRedraw):
            self.world.remove_component(entity, NeedRedraw)
