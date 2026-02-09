from dataclasses import dataclass

from ecs_framework.primitives import ComponentProtocol


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
class Trigger(ComponentProtocol):
    component: ComponentProtocol


@dataclass(slots=True)
class InputFilter(ComponentProtocol):
    allowed_chars: set[str]
