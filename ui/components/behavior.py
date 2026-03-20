from dataclasses import dataclass

from omniecs.types import Component


@dataclass(slots=True)
class Enabled(Component): ...


@dataclass(slots=True)
class Hoverable(Component): ...


@dataclass(slots=True)
class Hovered(Component): ...


@dataclass(slots=True)
class Pressable(Component): ...


@dataclass(slots=True)
class Pressed(Component): ...


@dataclass(slots=True)
class Focusable(Component): ...


@dataclass(slots=True)
class Focused(Component): ...


@dataclass(slots=True)
class Toggleable(Component): ...


@dataclass(slots=True)
class Toggled(Component): ...


@dataclass(slots=True)
class Selectable(Component): ...


@dataclass(slots=True)
class Selected(Component): ...


@dataclass(slots=True)
class SelectionGroup(Component):
    group: str


@dataclass(slots=True)
class Trigger(Component):
    component: Component


@dataclass(slots=True)
class Triggered(Component): ...


@dataclass(slots=True)
class InputFilter(Component):
    allowed_chars: set[str]


@dataclass(slots=True)
class HoverIntention(Component): ...


@dataclass(slots=True)
class PressIntent(Component): ...


@dataclass(slots=True)
class ActivateIntent(Component): ...
