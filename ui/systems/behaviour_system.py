from omniecs.components import Spawned
from omniecs.system import System

from ui.components.behavior import Focusable, Focused, Hoverable, Hovered, InputFilter, Pressable, Pressed, Selectable, Selected, SelectionGroup, Toggleable, Toggled, Trigger, Triggered
from ui.components.content import InputValue
from ui.components.intent import ActivateIntent, DeleteKeyIntent, EnterKeyIntent, HoverIntent, PressIntent, TextIntent
from ui.components.rendering import Dirty
from ui.components.style import BlinkingEffect
from ui.events.events import DeselectGroupEvent, LoseFocusEvent


class HoverSystem(System):

    def execute(self, _: float) -> None:
        for (entity_id, (hoverable,)) in self.world.query(Hoverable, all_of=(Hovered,), none_of=(HoverIntent,)):
            self.world.remove_component(entity_id, Hovered)
            for command in hoverable.exit:
                self.world.add_component(entity_id, command)

        for (entity_id, (hoverable,)) in self.world.query(Hoverable, all_of=(HoverIntent,), none_of=(Hovered,)):
            self.world.add_component(entity_id, Hovered())
            for command in hoverable.enter:
                self.world.add_component(entity_id, command)


class PressSystem(System):

    def execute(self, _: float) -> None:
        for (entity_id, (pressable,)) in self.world.query(Pressable, all_of=(PressIntent,)):
            self.world.add_component(entity_id, Pressed())
            for command in pressable.enter:
                self.world.add_component(entity_id, command)

        for (entity_id, (pressable,)) in self.world.query(Pressable, all_of=(Pressed,), none_of=(Hovered,)):
            self.world.remove_component(entity_id, Pressed)
            for command in pressable.exit:
                self.world.add_component(entity_id, command)


class ActivateSystem(System):

    def on_register(self) -> None:
        self.world.register_temporary_component(Triggered)

    def execute(self, _: float) -> None:
        for (entity_id, (pressable, trigger)) in self.world.query(Pressable, Trigger, all_of=(ActivateIntent,)):
            self.world.remove_component(entity_id, Pressed)
            for command in pressable.exit:
                self.world.add_component(entity_id, command)
                
            self.world.add_component(entity_id, Triggered())
            for command in trigger.commands:
                self.world.add_component(entity_id, command)


class SelectSystem(System):

    def execute(self, _: float) -> None:
        for (entity_id, (selectable,)) in self.world.query(Selectable, all_of=(PressIntent,)):
            self.world.add_component(entity_id, Selected())
            for command in selectable.enter:
                self.world.add_component(entity_id, command)

            selection_group: SelectionGroup = self.world.get_component(entity_id, SelectionGroup)
            if selection_group:
                self.world.push_event(DeselectGroupEvent(group=selection_group.group, selected=entity_id))

        for (entity_id, (selectable,)) in self.world.query(Selectable, all_of=(Selected, Spawned)):
            for command in selectable.enter:
                self.world.add_component(entity_id, command)


class DeselectSystem(System):

    def execute(self, _: float) -> None:
        for event in self.world.get_events():
            if not isinstance(event, DeselectGroupEvent):
                continue

            for (entity_id, (selectable, selection_group)) in self.world.query(Selectable, SelectionGroup, all_of=(Selected,)):
                if entity_id == event.selected or selection_group.group != event.group:
                    continue

                self.world.remove_component(entity_id, Selected)
                for command in selectable.exit:
                    self.world.add_component(entity_id, command)


class ToggleSystem(System):

    def execute(self, _: float) -> None:
        for (entity_id, (toggleable,)) in self.world.query(Toggleable, all_of=(PressIntent,)):
            if self.world.get_component(entity_id, Toggled):
                self.world.remove_component(entity_id, Toggled)
                for command in toggleable.exit:
                    self.world.add_component(entity_id, command)
            else:
                self.world.add_component(entity_id, Toggled())
                for command in toggleable.enter:
                    self.world.add_component(entity_id, command)

        for (entity_id, (toggleable,)) in self.world.query(Toggleable, all_of=(Toggled, Spawned)):
            for command in toggleable.enter:
                self.world.add_component(entity_id, command)
        

class FocusSystem(System):

    def execute(self, _: float) -> None:
        for (entity_id, (focusable,)) in self.world.query(Focusable, all_of=(Focused, Spawned)):
            for command in focusable.enter:
                self.world.add_component(entity_id, command)
            self.world.push_event(LoseFocusEvent(focused=entity_id))

        for entity_id in self.world.query_entities(all_of=(PressIntent,)):
            focusable = self.world.get_component(entity_id, Focusable)
            if focusable:
                self.world.add_component(entity_id, Focused())
                self.world.add_component(entity_id, Dirty())
                for command in focusable.enter:
                    self.world.add_component(entity_id, command)
            self.world.push_event(LoseFocusEvent(focused=entity_id))
        

class FocusBlinkSystem(System):

    def execute(self, delta_time: float) -> None:
        for (entity_id, (blinking,)) in self.world.query(BlinkingEffect, all_of=(Focused,)):
            blinking.timer += delta_time
            if blinking.timer > blinking.interval:
                blinking.timer -= blinking.interval
                blinking.visible = not blinking.visible
                self.world.add_component(entity_id, Dirty())


class UnfocusSystem(System):

    def execute(self, _: float) -> None:
        for event in self.world.get_events():
            if not isinstance(event, LoseFocusEvent):
                continue

            for (entity_id, (focusable,)) in self.world.query(Focusable, all_of=(Focused,)):
                if entity_id == event.focused:
                    continue

                self.world.remove_component(entity_id, Focused)
                self.world.add_component(entity_id, Dirty())
                for command in focusable.exit:
                    self.world.add_component(entity_id, command)


class TextInputSystem(System):

    def execute(self, _: float) -> None:
        for (entity_id, (text_input, input_value, input_filter)) in self.world.query(TextIntent, InputValue, InputFilter):
            filtered_text = [char for char in text_input.text if char in input_filter.allowed_chars]

            if filtered_text:
                input_value.value += ''.join(filtered_text)
                self.world.add_component(entity_id, Dirty())


class EnterKeySystem(System):

    def execute(self, _: float) -> None:
        for entity_id in self.world.query_entities(all_of=(Focused, EnterKeyIntent,)):
            self.world.remove_component(entity_id, Focused)
            self.world.add_component(entity_id, Dirty())


class DeleteKeySystem(System):

    def execute(self, _: float) -> None:
        for (entity_id, (input_value,)) in self.world.query(InputValue, all_of=(DeleteKeyIntent,)):
            input_value.value = input_value.value[:-1]
            self.world.add_component(entity_id, Dirty())
