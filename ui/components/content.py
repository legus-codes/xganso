from dataclasses import dataclass

from ecs_framework.types import Component


@dataclass(slots=True)
class Text(Component):
    text: str


@dataclass(slots=True)
class InputValue(Component):
    value: str
