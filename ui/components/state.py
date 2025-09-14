from dataclasses import dataclass
from typing import List

from ecs_framework.ecs import ComponentProtocol


@dataclass
class Enabled(ComponentProtocol):
    pass


@dataclass
class Hoverable(ComponentProtocol):
    pass


@dataclass
class Hovered(ComponentProtocol):
    pass


@dataclass
class Pressable(ComponentProtocol):
    pass


@dataclass
class Pressed(ComponentProtocol):
    pass


@dataclass
class Focusable(ComponentProtocol):
    pass


@dataclass
class Focused(ComponentProtocol):
    pass


@dataclass
class Toggleable(ComponentProtocol):
    pass


@dataclass
class Toggled(ComponentProtocol):
    pass


@dataclass
class Selectable(ComponentProtocol):
    pass


@dataclass
class Selected(ComponentProtocol):
    pass


@dataclass
class Typeable(ComponentProtocol):
    accepted_chars: List[str]
