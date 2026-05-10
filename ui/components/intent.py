from dataclasses import dataclass

from omniecs.types import Component


@dataclass(slots=True)
class HoverIntent(Component): ...


@dataclass(slots=True)
class PressIntent(Component): ...


@dataclass(slots=True)
class ActivateIntent(Component): ...


@dataclass(slots=True)
class TextIntent(Component):
    text: str


@dataclass(slots=True)
class EnterKeyIntent(Component): ...


@dataclass(slots=True)
class DeleteKeyIntent(Component): ...
