from adapters.input.events import KeyDown, KeyUp, MouseButtonDown, MouseButtonUp, MouseMove, TextInput
from omniecs.system import System
from ui.resources.state import KeyboardState, PointerState


class PointerStateSystem(System):

    def execute(self, _: float):
        pointer_state = self.world.get_resource(PointerState)
        pointer_state.reset()

        for event in self.world.get_events():
            if isinstance(event, MouseMove):
                pointer_state.position = event.position

            elif isinstance(event, MouseButtonDown):
                pointer_state.position = event.position
                pointer_state.buttons_pressed.add(event.button)
                pointer_state.buttons_down.add(event.button)

            elif isinstance(event, MouseButtonUp):
                pointer_state.position = event.position
                pointer_state.buttons_released.add(event.button)
                pointer_state.buttons_down.discard(event.button)


class KeyboardStateSystem(System):

    def execute(self, _: float):
        keyboard_state = self.world.get_resource(KeyboardState)
        keyboard_state.reset()

        for event in self.world.get_events():
            if isinstance(event, KeyDown):
                keyboard_state.keys_pressed.add(event.key)
                keyboard_state.keys_down.add(event.key)

            elif isinstance(event, KeyUp):
                keyboard_state.keys_released.add(event.key)
                keyboard_state.keys_down.discard(event.key)

            elif isinstance(event, TextInput):
                keyboard_state.text_input.append(event.text)
