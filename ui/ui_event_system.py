import pygame
from ecs_framework.ecs import ECS, SystemProtocol
from ui.keyboard_input import Key, KeyDown
from ui.mouse_input import MouseButton, MouseClicked, MousePosition, MousePressed, MouseReleased
from ui.ui_components import UICallback, UIEnabled, UIFocusable, UIFocused, UIHoverable, UIHovered, UINeedRedraw, UIPressable, UIPressed, UIRadioGroup, UIRect, UISelectable, UISelected, UIToggleable, UIToggled, UITypeable, UIVariable


class UIEventConverterSystem(SystemProtocol):

    def __init__(self, ecs: ECS, mouse: int, keyboard: int):
        self.ecs = ecs
        self.mouse = mouse
        self.keyboard = keyboard

    def execute(self, delta_time: float):
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
            elif event.type == pygame.KEYDOWN:
                self.ecs.add_component(self.keyboard, KeyDown(event.unicode, event.key))

            if event.type == pygame.QUIT:
                self.ecs.running = False

class UIMousePositionSystem(SystemProtocol):

    def __init__(self, ecs: ECS, mouse: int):
        self.ecs = ecs
        self.mouse = mouse

    def execute(self, delta_time: float):
        position_component = self.ecs.get_entity_component(self.mouse, MousePosition)
        mouse_position = position_component.position if position_component else None

        for entity in self.ecs.get_entities_with(UIEnabled, UIHoverable, UIRect):
            rect: UIRect = self.ecs.get_entity_component(entity, UIRect)
            if self.ecs.entity_has_component(entity, UIHovered):
                self.ecs.remove_component(entity, UIHovered)
                self.ecs.add_component(entity, UINeedRedraw())
            if mouse_position and rect.rectangle.collidepoint(mouse_position):
                self.ecs.add_component(entity, UIHovered())
                self.ecs.add_component(entity, UINeedRedraw())


class UIMouseClickedSystem(SystemProtocol):

    def __init__(self, ecs: ECS, mouse: int):
        self.ecs = ecs
        self.mouse = mouse

    def execute(self, delta_time: float):
        mouse_clicked = self.ecs.get_entity_component(self.mouse, MouseClicked)
        if mouse_clicked is None:
            return

        for entity in self.ecs.get_entities_with(UIEnabled, UIFocusable):
            hovered = self.ecs.get_entity_component(entity, UIHovered)
            if hovered:
                self.ecs.add_component(entity, UIFocused())
                self.ecs.add_component(entity, UINeedRedraw())
            elif self.ecs.entity_has_component(entity, UIFocused):
                self.ecs.remove_component(entity, UIFocused)
                self.ecs.add_component(entity, UINeedRedraw())

        for entity in self.ecs.get_entities_with(UIEnabled, UIToggleable, UIHovered):
            if self.ecs.entity_has_component(entity, UIToggled):
                self.ecs.remove_component(entity, UIToggled)
                self.ecs.add_component(entity, UINeedRedraw())
            else:
                self.ecs.add_component(entity, UIToggled())
                self.ecs.add_component(entity, UINeedRedraw())

        for entity in self.ecs.get_entities_with(UIEnabled, UISelectable, UIHovered):
            radio_group = self.ecs.get_entity_component(entity, UIRadioGroup)
            if radio_group:
                for other in self.ecs.get_entities_with(UIEnabled, UIRadioGroup):
                    other_radio = self.ecs.get_entity_component(other, UIRadioGroup)
                    if radio_group.name == other_radio.name and self.ecs.entity_has_component(other, UISelected):
                        self.ecs.remove_component(other, UISelected)
                        self.ecs.add_component(other, UINeedRedraw())
            self.ecs.add_component(entity, UISelected())
            self.ecs.add_component(entity, UINeedRedraw())

        self.ecs.remove_component(self.mouse, MouseClicked)


class UIMouseReleasedSystem(SystemProtocol):

    def __init__(self, ecs: ECS, mouse: int):
        self.ecs = ecs
        self.mouse = mouse

    def execute(self, delta_time: float):
        mouse_released = self.ecs.get_entity_component(self.mouse, MouseReleased)
        if mouse_released is None:
            return

        for entity in self.ecs.get_entities_with(UIEnabled, UIHovered, UIPressed):
            self.ecs.remove_component(entity, UIPressed)
            self.ecs.add_component(entity, UINeedRedraw())
            callback = self.ecs.get_entity_component(entity, UICallback)
            if callback:
                callback.callback()            

        self.ecs.remove_component(self.mouse, MouseReleased)


class UIMousePressedSystem(SystemProtocol):

    def __init__(self, ecs: ECS, mouse: int):
        self.ecs = ecs
        self.mouse = mouse

    def execute(self, delta_time: float):
        mouse_pressed = self.ecs.get_entity_component(self.mouse, MousePressed)
        if mouse_pressed is None:
            return

        for entity in self.ecs.get_entities_with(UIEnabled, UIPressable):
            if self.ecs.entity_has_component(entity, UIHovered):
                self.ecs.add_component(entity, UIPressed())
                self.ecs.add_component(entity, UINeedRedraw())
            elif self.ecs.entity_has_component(entity, UIPressed):
                self.ecs.remove_component(entity, UIPressed)
                self.ecs.add_component(entity, UINeedRedraw())


class UIKeyDownSystem(SystemProtocol):

    def __init__(self, ecs: ECS, keyboard: int):
        self.ecs = ecs
        self.keyboard = keyboard

    def execute(self, delta_time: float):
        key_down: KeyDown = self.ecs.get_entity_component(self.keyboard, KeyDown)
        if key_down is None:
            return
        
        for entity in self.ecs.get_entities_with(UIEnabled, UIFocused, UITypeable):
            if key_down.key == Key.ENTER.value:
                self.ecs.remove_component(entity, UIFocused)
                self.ecs.add_component(entity, UINeedRedraw())
            elif key_down.key == Key.DELETE.value:
                if not self.ecs.entity_has_component(entity, UIVariable):
                    continue

                variable: UIVariable = self.ecs.get_entity_component(entity, UIVariable)
                variable.value = variable.value[:-1]
                self.ecs.add_component(entity, UINeedRedraw())
            else:
                if not self.ecs.entity_has_component(entity, UIVariable):
                    continue

                variable: UIVariable = self.ecs.get_entity_component(entity, UIVariable)
                typeable: UITypeable = self.ecs.get_entity_component(entity, UITypeable)
                if key_down.char in typeable.accepted_chars:
                    variable.value += key_down.char
                    self.ecs.add_component(entity, UINeedRedraw())

        self.ecs.remove_component(self.keyboard, KeyDown)
