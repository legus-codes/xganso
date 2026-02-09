from dataclasses import dataclass

from ecs_framework.primitives import ComponentProtocol


@dataclass(slots=True)
class Text(ComponentProtocol):
    text: str


@dataclass(slots=True)
class InputValue(ComponentProtocol):
    value: str
