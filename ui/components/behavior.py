from typing import Set

from ecs_framework.ecs import ComponentProtocol


class Enabled(ComponentProtocol): ...


class Hoverable(ComponentProtocol): ...


class Hovered(ComponentProtocol): ...


class Pressable(ComponentProtocol): ...


class Pressed(ComponentProtocol): ...


class Focusable(ComponentProtocol): ...


class Focused(ComponentProtocol): ...


class Toggleable(ComponentProtocol): ...


class Toggled(ComponentProtocol): ...


class Selectable(ComponentProtocol): ...


class Selected(ComponentProtocol): ...


class SelectionGroup(ComponentProtocol):
    group: str


class Action(ComponentProtocol):
    name: str


class Typeable(ComponentProtocol):
    accepted_chars: Set[str]
