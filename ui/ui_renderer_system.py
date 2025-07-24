import pygame
from ecs_framework.ecs import ECS, SystemProtocol
from ui.ui_components import Allignment, UIColor, UIElement, UIEnabled, UIFocused, UIFont, UIForceRedraw, UIFrameable, UIHighlightable, UIHovered, UILabel, UILabelable, UINeedRedraw, UIPadding, UIParent, UIPressed, UIRect, UIRelativeRect, UIRenderLayer, UIRenderable, UISelected, UIText, UIToggled, UIVariable


def _center_middle_position(rect: pygame.Rect, text_rect: pygame.Surface) -> pygame.Vector2:
    x = rect.left + (rect.width - text_rect.get_width()) / 2
    y = rect.top + (rect.height - text_rect.get_height()) / 2
    return pygame.Vector2(x, y)


def _left_middle_position(rect: pygame.Rect, text_rect: pygame.Surface) -> pygame.Vector2:
    x = rect.left + 5
    y = rect.top + (rect.height - text_rect.get_height()) / 2
    return pygame.Vector2(x, y)


class UIRelativeToRect(SystemProtocol):

    def __init__(self, ecs: ECS):
        self.ecs = ecs

    def execute(self):
        for entity in self.ecs.get_entities_with(UIElement, UIEnabled, UIParent, UIRelativeRect):
            if self.ecs.entity_has_component(entity, UIRect):
                continue

            parent: UIParent = self.ecs.get_entity_component(entity, UIParent)
            if not self.ecs.entity_has_component(parent.entity, UIRect):
                continue

            relative_rect: UIRelativeRect = self.ecs.get_entity_component(entity, UIRelativeRect)
            parent_rect: UIRect = self.ecs.get_entity_component(parent.entity, UIRect)
            rect = UIRect(relative_rect.rectangle.move(parent_rect.rectangle.topleft))
            self.ecs.add_component(entity, rect)


class UIRendererSystem(SystemProtocol):

    def __init__(self, ecs: ECS, screen: pygame.Surface):
        self.ecs = ecs
        self.screen = screen

    def execute(self):
        all_entities = []
        for entity in self.ecs.get_entities_with(UIElement, UIEnabled, UIRenderable, UIColor, UIRect):
            render_layer: UIRenderLayer = self.ecs.get_entity_component(entity, UIRenderLayer)
            layer = render_layer.layer if render_layer is not None else 100
            all_entities.append((entity, layer))

        all_entities.sort(key=lambda x: x[1])

        for entity, layer in all_entities:
            if not (self.ecs.entity_has_component(entity, UIForceRedraw) or self.ecs.entity_has_component(entity, UINeedRedraw)):
                continue

            rect: UIRect = self.ecs.get_entity_component(entity, UIRect)
            colors: UIColor = self.ecs.get_entity_component(entity, UIColor)
            self.screen.set_clip(rect.rectangle)
            
            self.draw_background(entity, rect, colors)
            if self.ecs.entity_has_component(entity, UIHighlightable):
                self.draw_highlight(entity, rect, colors)
            if self.ecs.entity_has_component(entity, UILabelable):
                self.draw_text(entity, rect, colors)

            if self.ecs.entity_has_component(entity, UINeedRedraw):
                self.ecs.remove_component(entity, UINeedRedraw)
            self.screen.set_clip(None)


    def draw_background(self, entity: int, rect: UIRect, colors: UIColor) -> None:

        background = colors.background
        if self.ecs.entity_has_component(entity, UIToggled):
            background = colors.select
        if self.ecs.entity_has_component(entity, UISelected):
            background = colors.select
        if self.ecs.entity_has_component(entity, UIPressed):
            background = colors.press

        pygame.draw.rect(self.screen, background, rect.rectangle)

    def draw_highlight(self, entity: int, rect: UIRect, colors: UIColor) -> None:
        if self.ecs.entity_has_component(entity, UIFrameable):
            pygame.draw.rect(self.screen, colors.frame, rect.rectangle, 2)
        if self.ecs.entity_has_component(entity, UIHovered):
            pygame.draw.rect(self.screen, colors.hover, rect.rectangle, 2)
        if self.ecs.entity_has_component(entity, UIFocused):
            pygame.draw.rect(self.screen, colors.focus, rect.rectangle, 2)

    def draw_text(self, entity: int, rect: UIRect, colors: UIColor) -> None:
        if not self.ecs.entity_has_component(entity, UIFont):
            return

        font: UIFont = self.ecs.get_entity_component(entity, UIFont)

        padding: UIPadding = self.ecs.get_entity_component(entity, UIPadding)
        left_pad = padding.left if padding else 0
        top_pad = padding.top if padding else 0

        label_width: pygame.Vector2 = (0, 0)

        if self.ecs.entity_has_component(entity, UIText):
            text: UIText = self.ecs.get_entity_component(entity, UIText)

            text_position = rect.rectangle.topleft + pygame.Vector2(left_pad, top_pad)
            text_surface = font.font.render(text.text, True, colors.text)

            self.screen.blit(text_surface, text_position)

        if self.ecs.entity_has_component(entity, UILabel):
            label: UILabel = self.ecs.get_entity_component(entity, UILabel)

            label_surface = font.font.render(label.label, True, colors.text)
            if label.allignment == Allignment.left:
                label_position = _left_middle_position(rect.rectangle, label_surface)
            else:
                label_position = _center_middle_position(rect.rectangle, label_surface)
            label_width = pygame.Vector2(label_surface.get_width(), 0)
            self.screen.blit(label_surface, label_position)

        if self.ecs.entity_has_component(entity, UIVariable):
            variable: UIVariable = self.ecs.get_entity_component(entity, UIVariable)

            text_surface = font.font.render(variable.value, True, colors.text)
            text_position = _left_middle_position(rect.rectangle, text_surface) + label_width
            self.screen.blit(text_surface, text_position)

            if self.ecs.entity_has_component(entity, UIFocused):
                cursor_position = text_position.xy + pygame.Vector2(text_surface.get_width() + 2, 0)
                cursor_height = text_surface.get_height()
                pygame.draw.line(self.screen, colors.text, cursor_position, cursor_position + pygame.Vector2(0, cursor_height))
