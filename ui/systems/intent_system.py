from omniecs.system import System
from omniecs.types import EntityId

from adapters.input.events import Key, MouseButton
from core.primitives import Rect
from ui.components.behavior import Enabled, Focused, Hoverable, Hovered, Pressed
from ui.components.intent import ActivateIntent, DeleteKeyIntent, EnterKeyIntent, HoverIntent, PressIntent, TextIntent
from ui.components.layout import RenderLayer, WorldTransform
from ui.resources.state import KeyboardState, PointerState


class PointerHitTestSystem(System):

    def on_register(self) -> None:
        self.world.register_temporary_component(HoverIntent)

    def execute(self, _: float) -> None:
        pointer = self.world.get_resource(PointerState)

        elements: list[tuple[EntityId, tuple[WorldTransform, RenderLayer]]] = list(self.world.query(WorldTransform, RenderLayer, all_of=(Enabled, Hoverable)))
        elements.sort(key=lambda x: x[1][1].layer, reverse=True)

        for entity_id, (transform, _) in elements:
            rect = Rect.from_transform(transform.position, transform.size)
            if rect.contains(pointer.position):
                self.world.add_component(entity_id, HoverIntent())
                break


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


class TextIntentSystem(System):

    def on_register(self) -> None:
        self.world.register_temporary_component(TextIntent)

    def execute(self, _: float) -> None:
        keyboard = self.world.get_resource(KeyboardState)

        if not keyboard.text_input:
            return
        
        for entity_id in self.world.query_entities(all_of=(Focused,)):
            self.world.add_component(entity_id, TextIntent(text=keyboard.text_input))


class KeyIntentSystem(System):

    def on_register(self) -> None:
        self.world.register_temporary_component(EnterKeyIntent)
        self.world.register_temporary_component(DeleteKeyIntent)

    def execute(self, _: float) -> None:
        keyboard = self.world.get_resource(KeyboardState)
        
        for entity_id in self.world.query_entities(all_of=(Focused,)):
            if keyboard.was_pressed(Key.ENTER):
                self.world.add_component(entity_id, EnterKeyIntent())
            if keyboard.was_pressed(Key.DELETE):
                self.world.add_component(entity_id, DeleteKeyIntent())
