from collections import defaultdict

from omniecs.system import System

from adapters.input.events import Key, KeyDown, KeyUp, MouseButtonDown, MouseButtonUp, MouseMove, QuitRequested, TextInput
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

    press_time: int = 150

    def __init__(self):
        self._cooldown: dict[Key, float] = defaultdict(float)

    def execute(self, delta_time: float):
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

        for key in keyboard_state.keys_down:
            self._cooldown[key] += delta_time
            if self._cooldown[key] >= self.press_time:
                self._cooldown[key] -= self.press_time
                keyboard_state.keys_pressed.add(key)

        for key in self._cooldown.keys():
            if key not in keyboard_state.keys_down:
                self._cooldown[key] = 0


class ApplicationStateSystem(System):
     
     def execute(self, _: float):
        for event in self.world.get_events():
            if isinstance(event, QuitRequested):
                self.world._running = False
