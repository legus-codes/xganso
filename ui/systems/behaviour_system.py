from omniecs.system import System
from ui.components.behavior import Focusable, Focused, Hovered, InputFilter, Pressable, Pressed, Selectable, Selected, SelectionGroup, Toggleable, Toggled, Trigger, Triggered
from ui.components.content import InputValue
from ui.components.intent import ActivateIntent, DeleteKeyIntent, EnterKeyIntent, HoverIntent, PressIntent, TextIntent
from ui.components.rendering import Dirty
from ui.events.events import DeselectItemEvent
from ui.resources.state import WidgetState


class HoverSystem(System):

    def execute(self, _: float) -> None:
        widgets = self.world.get_resource(WidgetState)
        current_targets = self.world.query_entities(all_of=(HoverIntent,))
        
        for entity_id in widgets.hovered_entities.difference(current_targets):
            self.world.remove_component(entity_id, Hovered)
            self.world.add_component(entity_id, Dirty())
            widgets.hovered_entities.discard(entity_id)

        for entity_id in current_targets.difference(widgets.hovered_entities):
            self.world.add_component(entity_id, Hovered())
            self.world.add_component(entity_id, Dirty())
            widgets.hovered_entities.add(entity_id)

        self.world.set_resource(widgets)


class PressSystem(System):

    def execute(self, _: float) -> None:
        widgets = self.world.get_resource(WidgetState)

        for entity_id in self.world.query_entities(all_of=(PressIntent, Pressable)):
            self.world.add_component(entity_id, Pressed())
            self.world.add_component(entity_id, Dirty())
            widgets.active_entities.add(entity_id)

        for entity_id in self.world.query_entities(all_of=(Pressed,), none_of=(Hovered,)):
            self.world.remove_component(entity_id, Pressed)
            self.world.add_component(entity_id, Dirty())

        for entity_id in self.world.query_entities(all_of=(Hovered, Pressable), none_of=(Pressed,)):
            if entity_id in widgets.active_entities:
                self.world.add_component(entity_id, Pressed())
                self.world.add_component(entity_id, Dirty())

        self.world.set_resource(widgets)


class ActivateSystem(System):

    def on_register(self) -> None:
        self.world.register_temporary_component(Triggered)

    def execute(self, _: float) -> None:
        widgets = self.world.get_resource(WidgetState)

        for entity_id in self.world.query_entities(all_of=(ActivateIntent, Trigger)):
            self.world.remove_component(entity_id, Pressed)
            self.world.add_component(entity_id, Triggered())
            self.world.add_component(entity_id, Dirty())
            widgets.active_entities.clear()
            self.world.set_resource(widgets)


class SelectSystem(System):

    def execute(self, _: float) -> None:
        for entity_id in self.world.query_entities(all_of=(PressIntent, Selectable)):
            self.world.add_component(entity_id, Selected())
            self.world.add_component(entity_id, Dirty())

            selection_group: SelectionGroup = self.world.get_component(entity_id, SelectionGroup)
            if selection_group is None:
                continue
            
            self.world.push_event(DeselectItemEvent(radio_group=selection_group.group, selected_item=entity_id))


class DeselectSystem(System):

    def execute(self, _: float) -> None:
        for event in self.world.get_events():
            if not isinstance(event, DeselectItemEvent):
                continue

            for (entity_id, (selection_group,)) in self.world.query(SelectionGroup, all_of=(Selected,)):
                if entity_id == event.selected_item or selection_group.group != event.radio_group:
                    continue

                self.world.remove_component(entity_id, Selected)
                self.world.add_component(entity_id, Dirty())


class ToggleSystem(System):

    def execute(self, _: float) -> None:
        for entity_id in self.world.query_entities(all_of=(PressIntent, Toggleable)):
            if self.world.get_component(entity_id, Toggled):
                self.world.remove_component(entity_id, Toggled)
            else:
                self.world.add_component(entity_id, Toggled())
            self.world.add_component(entity_id, Dirty())
        

class FocusSystem(System):

    def execute(self, _: float) -> None:
        for entity_id in self.world.query_entities(all_of=(PressIntent,)):
            if self.world.get_component(entity_id, Focusable):
                self.world.add_component(entity_id, Focused())
                self.world.add_component(entity_id, Dirty())

            for other_entity_id in self.world.query_entities(all_of=(Focused,), none_of=(PressIntent,)):
                self.world.remove_component(other_entity_id, Focused)
                self.world.add_component(other_entity_id, Dirty())


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
