from omniecs.system import System
from ui.components.behavior import ActivateIntent, HoverIntention, Hovered, PressIntent, Pressable, Pressed, Trigger, Triggered
from ui.resources.state import PointerState


class HoverSystem(System):

    def execute(self, _: float) -> None:
        pointer = self.world.get_resource(PointerState)
        current_targets = self.world.query_entities(all_of=(HoverIntention,))
        
        for entity_id in pointer.hovered_entities.difference(current_targets):
            self.world.remove_component(entity_id, Hovered)
            pointer.hovered_entities.discard(entity_id)

        for entity_id in current_targets.difference(pointer.hovered_entities):
            self.world.add_component(entity_id, Hovered())
            pointer.hovered_entities.add(entity_id)

        self.world.set_resource(pointer)


class PressSystem(System):

    def on_register(self) -> None:
        self.world.register_temporary_component(Pressed)

    def execute(self, _: float) -> None:
        for entity_id in self.world.query_entities(all_of=(PressIntent, Pressable)):
            self.world.add_component(entity_id, Pressed())


class ActivateSystem(System):

    def on_register(self) -> None:
        self.world.register_temporary_component(Triggered)

    def execute(self, _: float) -> None:
        for entity_id in self.world.query_entities(all_of=(ActivateIntent, Trigger)):
            self.world.add_component(entity_id, Triggered())
