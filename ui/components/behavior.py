from dataclasses import dataclass
from typing import Set

from ecs_framework.ecs import ComponentProtocol


@dataclass(slots=True)
class Enabled(ComponentProtocol): ...


@dataclass(slots=True)
class Hoverable(ComponentProtocol): ...


@dataclass(slots=True)
class Hovered(ComponentProtocol): ...


@dataclass(slots=True)
class Pressable(ComponentProtocol): ...


@dataclass(slots=True)
class Pressed(ComponentProtocol): ...


@dataclass(slots=True)
class Focusable(ComponentProtocol): ...


@dataclass(slots=True)
class Focused(ComponentProtocol): ...


@dataclass(slots=True)
class Toggleable(ComponentProtocol): ...


@dataclass(slots=True)
class Toggled(ComponentProtocol): ...


@dataclass(slots=True)
class Selectable(ComponentProtocol): ...


@dataclass(slots=True)
class Selected(ComponentProtocol): ...


@dataclass(slots=True)
class SelectionGroup(ComponentProtocol):
    group: str


@dataclass(slots=True)
class Action(ComponentProtocol):
    name: str


@dataclass(slots=True)
class Typeable(ComponentProtocol):
    accepted_chars: Set[str]
