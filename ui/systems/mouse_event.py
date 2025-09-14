from ecs_framework.ecs import ECS, SystemProtocol
from ui.components.data import Trigger, RadioItem
from ui.components.input import MouseClicked, MousePosition, MousePressed, MouseReleased
from ui.components.layout import Rect
from ui.components.rendering import NeedRedraw
from ui.components.state import Enabled, Focusable, Focused, Hoverable, Hovered, Pressable, Pressed, Selectable, Selected, Toggleable, Toggled


class MouseHoverSystem(SystemProtocol):

    def __init__(self, world: ECS, mouse: int):
        self.world = world
        self.mouse = mouse

    def execute(self, delta_time: float):
        position_component = self.world.get_entity_component(self.mouse, MousePosition)
        mouse_position = position_component.position if position_component else None

        for entity, (rect, _, _) in self.world.get_entities_with_components(Rect, Enabled, Hoverable):
            if self.world.entity_has_component(entity, Hovered):
                self.world.remove_component(entity, Hovered)
                self.world.add_component(entity, NeedRedraw())
            if mouse_position and rect.rectangle.collidepoint(mouse_position):
                self.world.add_component(entity, Hovered())
                self.world.add_component(entity, NeedRedraw())


class MouseFocusSystem(SystemProtocol):

    def __init__(self, world: ECS, mouse: int):
        self.world = world
        self.mouse = mouse

    def execute(self, delta_time: float):
        mouse_clicked = self.world.get_entity_component(self.mouse, MouseClicked)
        if mouse_clicked is None:
            return

        for entity in self.world.get_entities_with(Enabled, Focusable):
            hovered = self.world.get_entity_component(entity, Hovered)
            if hovered:
                self.world.add_component(entity, Focused())
                self.world.add_component(entity, NeedRedraw())
            elif self.world.entity_has_component(entity, Focused):
                self.world.remove_component(entity, Focused)
                self.world.add_component(entity, NeedRedraw())


class MouseToggleSystem(SystemProtocol):

    def __init__(self, world: ECS, mouse: int):
        self.world = world
        self.mouse = mouse

    def execute(self, delta_time: float):
        mouse_clicked = self.world.get_entity_component(self.mouse, MouseClicked)
        if mouse_clicked is None:
            return
        
        for entity in self.world.get_entities_with(Enabled, Toggleable, Hovered):
            if self.world.entity_has_component(entity, Toggled):
                self.world.remove_component(entity, Toggled)
                self.world.add_component(entity, NeedRedraw())
            else:
                self.world.add_component(entity, Toggled())
                self.world.add_component(entity, NeedRedraw())


class MouseSelectSystem(SystemProtocol):

    def __init__(self, world: ECS, mouse: int):
        self.world = world
        self.mouse = mouse

    def execute(self, delta_time: float):        
        mouse_clicked = self.world.get_entity_component(self.mouse, MouseClicked)
        if mouse_clicked is None:
            return
        
        for entity in self.world.get_entities_with(Enabled, Selectable, Hovered):

            radio_item = self.world.get_entity_component(entity, RadioItem)
            if radio_item:
                for other_entity, (other_radio, _) in self.world.get_entities_with_components(RadioItem, Enabled):
                    if radio_item.radio_group == other_radio.radio_group and self.world.entity_has_component(other_entity, Selected):
                        self.world.remove_component(other_entity, Selected)
                        self.world.add_component(other_entity, NeedRedraw())

            self.world.add_component(entity, Selected())
            self.world.add_component(entity, NeedRedraw())


class CleanupMouseClickedSystem(SystemProtocol):

    def __init__(self, world: ECS, mouse: int):
        self.world = world
        self.mouse = mouse

    def execute(self, delta_time: float):
        self.world.remove_component(self.mouse, MouseClicked)


class MouseReleasedSystem(SystemProtocol):

    def __init__(self, world: ECS, mouse: int):
        self.world = world
        self.mouse = mouse

    def execute(self, delta_time: float):
        mouse_released = self.world.get_entity_component(self.mouse, MouseReleased)
        if mouse_released is None:
            return

        for entity in self.world.get_entities_with(Enabled, Hovered, Pressed):
            self.world.remove_component(entity, Pressed)
            self.world.add_component(entity, NeedRedraw())
            trigger = self.world.get_entity_component(entity, Trigger)
            if trigger:
                self.world.add_component(entity, trigger.name())


class CleanupMouseReleasedSystem(SystemProtocol):

    def __init__(self, world: ECS, mouse: int):
        self.world = world
        self.mouse = mouse

    def execute(self, delta_time: float):
        self.world.remove_component(self.mouse, MouseReleased)


class MousePressedSystem(SystemProtocol):

    def __init__(self, world: ECS, mouse: int):
        self.world = world
        self.mouse = mouse

    def execute(self, delta_time: float):
        mouse_pressed = self.world.get_entity_component(self.mouse, MousePressed)
        if mouse_pressed is None:
            return

        for entity in self.world.get_entities_with(Enabled, Pressable):
            if self.world.entity_has_component(entity, Hovered):
                self.world.add_component(entity, Pressed())
                self.world.add_component(entity, NeedRedraw())
            elif self.world.entity_has_component(entity, Pressed):
                self.world.remove_component(entity, Pressed)
                self.world.add_component(entity, NeedRedraw())
