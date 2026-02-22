from adapters.input.events import MouseButton
from ecs_framework.system import System
from ui.components.behavior import ActivateIntent, Hovered, PressIntent, Pressed
from ui.resources.state import PointerState


class PressIntentSystem(System):

    def on_register(self) -> None:
        self.world.register_temporary_component(PressIntent)

    def execute(self, _: float) -> None:
        pointer = self.world.get_resource(PointerState)

        if not pointer.was_pressed(MouseButton.left):
            return
        
        for entity_id in self.world.query_entities(all_of=(Hovered,)):
            self.world.add_component(entity_id, PressIntent())


class ActivateIntentSystem(System):

    def on_register(self) -> None:
        self.world.register_temporary_component(ActivateIntent)

    def execute(self, _: float) -> None:
        pointer = self.world.get_resource(PointerState)

        if not pointer.was_released(MouseButton.left):
            return
        
        for entity_id in self.world.query_entities(all_of=(Hovered, Pressed)):
            self.world.add_component(entity_id, ActivateIntent())
