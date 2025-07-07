import pygame
from ecs_framework.ecs import ECS, SystemProtocol
from ui.mouse_input import MouseButton, MouseClicked, MousePosition, MousePressed, MouseReleased
from ui.ui_components import Allignment, UICallback, UIColor, UIElement, UIEnabled, UIFocusable, UIFocused, UIFont, UIHoverable, UIHovered, UIInt, UILabel, UIPadding, UIPressable, UIPressed, UIRadioGroup, UIRect, UISelectable, UISelected, UIString, UIText, UIToggleable, UIToggled


def _center_middle_position(rect: pygame.Rect, text_rect: pygame.Surface) -> pygame.Vector2:
    x = rect.left + (rect.width - text_rect.get_width()) / 2
    y = rect.top + (rect.height - text_rect.get_height()) / 2
    return pygame.Vector2(x, y)


def _left_middle_position(rect: pygame.Rect, text_rect: pygame.Surface) -> pygame.Vector2:
    x = rect.left + 5
    y = rect.top + (rect.height - text_rect.get_height()) / 2
    return pygame.Vector2(x, y)


class UIBackgroundRendererSystem(SystemProtocol):

    def __init__(self, ecs: ECS, screen: pygame.Surface):
        self.ecs = ecs
        self.screen = screen

    def execute(self):
        for entity in self.ecs.get_entities_with(UIElement, UIEnabled, UIColor, UIRect):
            rect: UIRect = self.ecs.get_entity_component(entity, UIRect)
            colors: UIColor = self.ecs.get_entity_component(entity, UIColor)

            background = colors.background
            if self.ecs.entity_has_component(entity, UIToggled):
                background = colors.select
            if self.ecs.entity_has_component(entity, UISelected):
                background = colors.select
            if self.ecs.entity_has_component(entity, UIPressed):
                background = colors.press

            pygame.draw.rect(self.screen, background, rect.rectangle)


class UIHighlightRendererSystem(SystemProtocol):

    def __init__(self, ecs: ECS, screen: pygame.Surface):
        self.ecs = ecs
        self.screen = screen

    def execute(self):
        for entity in self.ecs.get_entities_with(UIElement, UIEnabled, UIHovered, UIColor, UIRect):
            rect: UIRect = self.ecs.get_entity_component(entity, UIRect)
            colors: UIColor = self.ecs.get_entity_component(entity, UIColor)
            pygame.draw.rect(self.screen, colors.hover, rect.rectangle, 2)

        for entity in self.ecs.get_entities_with(UIElement, UIEnabled, UIFocused, UIColor, UIRect):
            rect: UIRect = self.ecs.get_entity_component(entity, UIRect)
            colors: UIColor = self.ecs.get_entity_component(entity, UIColor)
            pygame.draw.rect(self.screen, colors.focus, rect.rectangle, 2)


class UITextRendererSystem(SystemProtocol):

    def __init__(self, ecs: ECS, screen: pygame.Surface):
        self.ecs = ecs
        self.screen = screen

    def execute(self):
        for entity in self.ecs.get_entities_with(UIElement, UIEnabled, UIColor, UIRect, UIText, UIFont):
            rect: UIRect = self.ecs.get_entity_component(entity, UIRect)
            colors: UIColor = self.ecs.get_entity_component(entity, UIColor)
            text: UIText = self.ecs.get_entity_component(entity, UIText)
            font: UIFont = self.ecs.get_entity_component(entity, UIFont)
            padding: UIPadding = self.ecs.get_entity_component(entity, UIPadding)
            left_pad = padding.left if padding else 0
            top_pad = padding.top if padding else 0

            text_position = rect.rectangle.topleft + pygame.Vector2(left_pad, top_pad)
            text_surface = font.font.render(text.text, True, colors.text)

            self.screen.blit(text_surface, text_position)

        for entity in self.ecs.get_entities_with(UIElement, UIEnabled, UIColor, UIRect, UILabel, UIFont):
            rect: UIRect = self.ecs.get_entity_component(entity, UIRect)
            colors: UIColor = self.ecs.get_entity_component(entity, UIColor)
            text: UIText = self.ecs.get_entity_component(entity, UIText)
            font: UIFont = self.ecs.get_entity_component(entity, UIFont)
            padding: UIPadding = self.ecs.get_entity_component(entity, UIPadding)
            left_pad = padding.left if padding else 0
            top_pad = padding.top if padding else 0

            label: UILabel = self.ecs.get_entity_component(entity, UILabel)
            font: UIFont = self.ecs.get_entity_component(entity, UIFont)

            label_surface = font.font.render(label.label, True, colors.text)
            if label.allignment == Allignment.left:
                label_position = _left_middle_position(rect.rectangle, label_surface)
            else:
                label_position = _center_middle_position(rect.rectangle, label_surface)
            self.screen.blit(label_surface, label_position)

        for entity in self.ecs.get_entities_with(UIElement, UIEnabled, UIColor, UIRect, UIString, UIFont):
            rect: UIRect = self.ecs.get_entity_component(entity, UIRect)
            colors: UIColor = self.ecs.get_entity_component(entity, UIColor)
            text: UIText = self.ecs.get_entity_component(entity, UIText)
            font: UIFont = self.ecs.get_entity_component(entity, UIFont)
            padding: UIPadding = self.ecs.get_entity_component(entity, UIPadding)
            left_pad = padding.left if padding else 0
            top_pad = padding.top if padding else 0

            variable: UIString = self.ecs.get_entity_component(entity, UIString)
            font: UIFont = self.ecs.get_entity_component(entity, UIFont)

            text_surface = font.font.render(variable.variable, True, colors.text)
            text_position = _center_middle_position(rect.rectangle, text_surface)
            self.screen.blit(text_surface, text_position)

            if self.ecs.entity_has_component(entity, UIFocused):
                cursor_position = text_position.xy + pygame.Vector2(text_surface.get_width() + 2, 0)
                cursor_height = text_surface.get_height()
                pygame.draw.line(self.screen, colors.text, cursor_position, cursor_position + pygame.Vector2(0, cursor_height))

        for entity in self.ecs.get_entities_with(UIElement, UIEnabled, UIColor, UIRect, UIInt, UIFont):
            rect: UIRect = self.ecs.get_entity_component(entity, UIRect)
            colors: UIColor = self.ecs.get_entity_component(entity, UIColor)
            text: UIText = self.ecs.get_entity_component(entity, UIText)
            font: UIFont = self.ecs.get_entity_component(entity, UIFont)
            padding: UIPadding = self.ecs.get_entity_component(entity, UIPadding)
            left_pad = padding.left if padding else 0
            top_pad = padding.top if padding else 0

            variable: UIInt = self.ecs.get_entity_component(entity, UIInt)
            font: UIFont = self.ecs.get_entity_component(entity, UIFont)

            text_surface = font.font.render(str(variable.variable), True, colors.text)
            text_position = _center_middle_position(rect.rectangle, text_surface)
            self.screen.blit(text_surface, text_position)

            if self.ecs.entity_has_component(entity, UIFocused):
                cursor_position = text_position.xy + pygame.Vector2(text_surface.get_width() + 2, 0)
                cursor_height = text_surface.get_height()
                pygame.draw.line(self.screen, colors.text, cursor_position, cursor_position + pygame.Vector2(0, cursor_height))


class UIEventConverterSystem(SystemProtocol):

    def __init__(self, ecs: ECS, mouse: int):
        self.ecs = ecs
        self.mouse = mouse

    def execute(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                self.ecs.add_component(self.mouse, MousePosition(event.pos))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.ecs.add_component(self.mouse, MouseClicked(MouseButton.left, event.pos))
                    self.ecs.add_component(self.mouse, MousePressed(MouseButton.left))
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.ecs.add_component(self.mouse, MouseReleased(MouseButton.left, event.pos))
                    self.ecs.remove_component(self.mouse, MousePressed)

            if event.type == pygame.QUIT:
                self.ecs.running = False

class UIMousePositionSystem(SystemProtocol):

    def __init__(self, ecs: ECS, mouse: int):
        self.ecs = ecs
        self.mouse = mouse

    def execute(self):
        position_component = self.ecs.get_entity_component(self.mouse, MousePosition)
        mouse_position = position_component.position if position_component else None

        for entity in self.ecs.get_entities_with(UIEnabled, UIHoverable, UIRect):
            rect: UIRect = self.ecs.get_entity_component(entity, UIRect)
            self.ecs.remove_component(entity, UIHovered)
            if mouse_position and rect.rectangle.collidepoint(mouse_position):
                self.ecs.add_component(entity, UIHovered())


class UIMouseClickedSystem(SystemProtocol):

    def __init__(self, ecs: ECS, mouse: int):
        self.ecs = ecs
        self.mouse = mouse

    def execute(self):
        mouse_clicked = self.ecs.get_entity_component(self.mouse, MouseClicked)
        if mouse_clicked is None:
            return

        for entity in self.ecs.get_entities_with(UIEnabled, UIFocusable):
            hovered = self.ecs.get_entity_component(entity, UIHovered)
            if hovered:
                self.ecs.add_component(entity, UIFocused())
            else:
                self.ecs.remove_component(entity, UIFocused)

        for entity in self.ecs.get_entities_with(UIEnabled, UIToggleable, UIHovered):
            if self.ecs.entity_has_component(entity, UIToggled):
                self.ecs.remove_component(entity, UIToggled)
            else:
                self.ecs.add_component(entity, UIToggled())

        for entity in self.ecs.get_entities_with(UIEnabled, UISelectable, UIHovered):
            radio_group = self.ecs.get_entity_component(entity, UIRadioGroup)
            if radio_group:
                for other in self.ecs.get_entities_with(UIEnabled, UIRadioGroup):
                    other_radio = self.ecs.get_entity_component(other, UIRadioGroup)
                    if radio_group.name == other_radio.name:
                        self.ecs.remove_component(other, UISelected)
            self.ecs.add_component(entity, UISelected())

        self.ecs.remove_component(self.mouse, MouseClicked)


class UIMouseReleasedSystem(SystemProtocol):

    def __init__(self, ecs: ECS, mouse: int):
        self.ecs = ecs
        self.mouse = mouse

    def execute(self):
        mouse_released = self.ecs.get_entity_component(self.mouse, MouseReleased)
        if mouse_released is None:
            return

        for entity in self.ecs.get_entities_with(UIEnabled, UIHovered, UIPressed):
            self.ecs.remove_component(entity, UIPressed)
            callback = self.ecs.get_entity_component(entity, UICallback)
            if callback:
                callback.callback()            

        self.ecs.remove_component(self.mouse, MouseReleased)


class UIMousePressedSystem(SystemProtocol):

    def __init__(self, ecs: ECS, mouse: int):
        self.ecs = ecs
        self.mouse = mouse

    def execute(self):
        mouse_pressed = self.ecs.get_entity_component(self.mouse, MousePressed)
        if mouse_pressed is None:
            return

        for entity in self.ecs.get_entities_with(UIEnabled, UIHovered, UIPressable):
            self.ecs.add_component(entity, UIPressed())
