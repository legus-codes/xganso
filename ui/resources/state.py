from dataclasses import dataclass

from core.primitives import IVec2
from ecs_framework.types import Resource
from adapters.input.events import MouseButton


@dataclass(slots=True)
class PointerState(Resource):
    position: IVec2
    buttons_down: set[MouseButton]
    buttons_pressed: set[MouseButton]
    buttons_released: set[MouseButton]

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
    keys_down: set[int]
    keys_pressed: set[int]
    keys_released: set[int]
    text_input: list[str]

    def is_down(self, key: int) -> bool:
        return key in self.keys_down

    def was_pressed(self, key: int) -> bool:
        return key in self.keys_pressed

    def was_released(self, key: int) -> bool:
        return key in self.keys_released

    def reset(self) -> None:
        self.keys_pressed.clear()
        self.keys_released.clear()
        self.text_input.clear()
