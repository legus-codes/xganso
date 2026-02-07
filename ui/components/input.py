from dataclasses import dataclass

from core.primitives import IVec2
from ecs_framework.ecs import ComponentProtocol
from ui.events.input import MouseButton


@dataclass(slots=True)
class MousePress(ComponentProtocol):
    position: IVec2
    button: MouseButton
