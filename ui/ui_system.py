import pygame
from ecs_framework.ecs import ECS, SystemProtocol
from ui.ui_components import UICallback, UIColor, UIElement, UIFont, UIInt, UILabel, UIPadding, UIRect, UIState, UIString, UIText


class UIRendererSystem(SystemProtocol):

    def __init__(self, ecs: ECS, screen: pygame.Surface):
        self.ecs = ecs
        self.screen = screen

    def execute(self):
        for entity in self.ecs.get_entities_with(UIElement, UIText, UIState, UIColor, UIFont, UIRect):
            self.draw_text(entity)

        for entity in self.ecs.get_entities_with(UIElement, UICallback, UILabel, UIState, UIColor, UIFont, UIRect):
            self.draw_button(entity)

        for entity in self.ecs.get_entities_with(UIElement, UILabel, UIString, UIState, UIColor, UIFont, UIRect):
            self.draw_text_input(entity)

        for entity in self.ecs.get_entities_with(UIElement, UILabel, UIInt, UIState, UIColor, UIFont, UIRect):
            self.draw_int_text_input(entity)

        for entity in self.ecs.get_entities_with(UIElement, UILabel, UIState, UIColor, UIFont, UIRect):
            self.draw_radio(entity)        

    
    def draw_text(self, entity: int):
        state: UIState = self.ecs.get_entity_component(entity, UIState)
        if not state.enabled:
            return
        
        rect: UIRect = self.ecs.get_entity_component(entity, UIRect)
        colors: UIColor = self.ecs.get_entity_component(entity, UIColor)
        
        pygame.draw.rect(self.screen, colors.background, rect.rectangle)

        text: UIText = self.ecs.get_entity_component(entity, UIText)
        font: UIFont = self.ecs.get_entity_component(entity, UIFont)
        padding: UIPadding = self.ecs.get_entity_component(entity, UIPadding)
        left_pad = padding.left if padding else 0
        top_pad = padding.top if padding else 0

        text_position = rect.rectangle.topleft + pygame.Vector2(left_pad, top_pad)
        text_surface = font.font.render(text.text, True, colors.text)

        self.screen.blit(text_surface, text_position)

    def draw_button(self, entity: int):
        state: UIState = self.ecs.get_entity_component(entity, UIState)
        if not state.enabled:
            return
        
        rect: UIRect = self.ecs.get_entity_component(entity, UIRect)
        colors: UIColor = self.ecs.get_entity_component(entity, UIColor)

        background_color = colors.background
        if state.pressed and state.hovered:
            background_color = colors.press

        pygame.draw.rect(self.screen, background_color, rect.rectangle)
        if state.hovered:
            pygame.draw.rect(self.screen, colors.hover, rect.rectangle, 2)

        label: UILabel = self.ecs.get_entity_component(entity, UILabel)
        font: UIFont = self.ecs.get_entity_component(entity, UIFont)

        label_surface = font.font.render(label.label, True, colors.text)
        label_position = self._center_middle_position(rect.rectangle, label_surface)
        self.screen.blit(label_surface, label_position)

    def draw_text_input(self, entity: int):
        state: UIState = self.ecs.get_entity_component(entity, UIState)
        if not state.enabled:
            return
        
        rect: UIRect = self.ecs.get_entity_component(entity, UIRect)
        colors: UIColor = self.ecs.get_entity_component(entity, UIColor)

        pygame.draw.rect(self.screen, colors.background, rect.rectangle)
        if state.focused:
            pygame.draw.rect(self.screen, colors.select, rect.rectangle, 2)
        elif state.hovered:
            pygame.draw.rect(self.screen, colors.hover, rect.rectangle, 2)

        label: UILabel = self.ecs.get_entity_component(entity, UILabel)
        variable: UIString = self.ecs.get_entity_component(entity, UIString)
        font: UIFont = self.ecs.get_entity_component(entity, UIFont)

        label_surface = font.font.render(label.label, True, colors.text)
        label_position = self._left_middle_position(rect.rectangle, label_surface)
        self.screen.blit(label_surface, label_position)

        text_surface = font.font.render(variable.variable, True, colors.text)
        text_position = self._left_middle_position(rect.rectangle, text_surface) + pygame.Vector2(label_surface.get_width(), 0)
        self.screen.blit(text_surface, text_position)

        if state.focused:
            cursor_position = text_position.xy + pygame.Vector2(text_surface.get_width() + 2, 0)
            cursor_height = text_surface.get_height()
            pygame.draw.line(self.screen, colors.text, cursor_position, cursor_position + pygame.Vector2(0, cursor_height))


    def draw_int_text_input(self, entity: int):
        state: UIState = self.ecs.get_entity_component(entity, UIState)
        if not state.enabled:
            return
        
        rect: UIRect = self.ecs.get_entity_component(entity, UIRect)
        colors: UIColor = self.ecs.get_entity_component(entity, UIColor)

        pygame.draw.rect(self.screen, colors.background, rect.rectangle)
        if state.focused:
            pygame.draw.rect(self.screen, colors.select, rect.rectangle, 2)
        elif state.hovered:
            pygame.draw.rect(self.screen, colors.hover, rect.rectangle, 2)

        label: UILabel = self.ecs.get_entity_component(entity, UILabel)
        variable: UIInt = self.ecs.get_entity_component(entity, UIInt)
        font: UIFont = self.ecs.get_entity_component(entity, UIFont)

        label_surface = font.font.render(label.label, True, colors.text)
        label_position = self._left_middle_position(rect.rectangle, label_surface)
        self.screen.blit(label_surface, label_position)

        text_surface = font.font.render(str(variable.variable), True, colors.text)
        text_position = self._left_middle_position(rect.rectangle, text_surface) + pygame.Vector2(label_surface.get_width(), 0)
        self.screen.blit(text_surface, text_position)

        if state.focused:
            cursor_position = text_position.xy + pygame.Vector2(text_surface.get_width() + 2, 0)
            cursor_height = text_surface.get_height()
            pygame.draw.line(self.screen, colors.text, cursor_position, cursor_position + pygame.Vector2(0, cursor_height))


    def draw_radio(self, entity: int):
        state: UIState = self.ecs.get_entity_component(entity, UIState)
        if not state.enabled:
            return
        
        rect: UIRect = self.ecs.get_entity_component(entity, UIRect)
        colors: UIColor = self.ecs.get_entity_component(entity, UIColor)

        background_color = colors.select if state.selected else colors.background
        pygame.draw.rect(self.screen, background_color, rect.rectangle)
        if state.hovered:
            pygame.draw.rect(self.screen, colors.hover, rect.rectangle, 2)

        label: UILabel = self.ecs.get_entity_component(entity, UILabel)
        font: UIFont = self.ecs.get_entity_component(entity, UIFont)

        label_surface = font.font.render(label.label, True, colors.text)
        label_position = self._center_middle_position(rect.rectangle, label_surface)
        self.screen.blit(label_surface, label_position)


    def _center_middle_position(self, rect: pygame.Rect, text_rect: pygame.Surface) -> pygame.Vector2:
        x = rect.left + (rect.width - text_rect.get_width()) / 2
        y = rect.top + (rect.height - text_rect.get_height()) / 2
        return pygame.Vector2(x, y)
    
    def _left_middle_position(self, rect: pygame.Rect, text_rect: pygame.Surface) -> pygame.Vector2:
        x = rect.left + 5
        y = rect.top + (rect.height - text_rect.get_height()) / 2
        return pygame.Vector2(x, y)

