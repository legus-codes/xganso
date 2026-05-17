from dataclasses import dataclass, field

from core.primitives import IVec2
from omniecs.types import Resource
from adapters.input.events import Key, MouseButton


@dataclass(slots=True)
class PointerState(Resource):
    position: IVec2 = field(default_factory=IVec2)
    buttons_down: set[MouseButton] = field(default_factory=set)
    buttons_pressed: set[MouseButton] = field(default_factory=set)
    buttons_released: set[MouseButton] = field(default_factory=set)

    def is_down(self, button: MouseButton) -> bool:
        return button in self.buttons_down

    def was_pressed(self, button: MouseButton) -> bool:
        return button in self.buttons_pressed

    def was_released(self, button: MouseButton) -> bool:
        return button in self.buttons_released

    def reset(self) -> None:
        self.buttons_pressed.clear()
        self.buttons_released.clear()


@dataclass(slots=True)
class KeyboardState(Resource):
    keys_down: set[Key] = field(default_factory=set)
    keys_pressed: set[Key] = field(default_factory=set)
    keys_released: set[Key] = field(default_factory=set)
    text_input: list[str] = field(default_factory=list)

    def is_down(self, key: Key) -> bool:
        return key in self.keys_down

    def was_pressed(self, key: Key) -> bool:
        return key in self.keys_pressed

    def was_released(self, key: Key) -> bool:
        return key in self.keys_released

    def reset(self) -> None:
        self.keys_pressed.clear()
        self.keys_released.clear()
        self.text_input.clear()
