from dataclasses import dataclass, field

from omniecs.types import Component

from ui.components.command import UICommand


@dataclass(slots=True)
class Enabled(Component): ...


@dataclass(slots=True)
class Hoverable(Component):
    enter: list[UICommand] = field(default_factory=list)
    exit: list[UICommand] = field(default_factory=list)


@dataclass(slots=True)
class Hovered(Component): ...


@dataclass(slots=True)
class Pressable(Component):
    enter: list[UICommand] = field(default_factory=list)
    exit: list[UICommand] = field(default_factory=list)


@dataclass(slots=True)
class Pressed(Component): ...


@dataclass(slots=True)
class Trigger(Component):
    commands: list[UICommand] = field(default_factory=list)


@dataclass(slots=True)
class Triggered(Component): ...


@dataclass(slots=True)
class Focusable(Component): ...


@dataclass(slots=True)
class Focused(Component): ...


@dataclass(slots=True)
class Toggleable(Component): ...


@dataclass(slots=True)
class Toggled(Component): ...


@dataclass(slots=True)
class Selectable(Component):
    enter: list[UICommand] = field(default_factory=list)
    exit: list[UICommand] = field(default_factory=list)


@dataclass(slots=True)
class Selected(Component): ...


@dataclass(slots=True)
class SelectionGroup(Component):
    group: str


@dataclass(slots=True)
class InputFilter(Component):
    allowed_chars: set[str]
