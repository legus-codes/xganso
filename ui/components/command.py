from dataclasses import dataclass

from omniecs.types import Component

from core.primitives import Color


@dataclass
class UICommand(Component): ...


@dataclass
class SetFrameColorCommand(UICommand):
    color: Color

@dataclass
class UnsetFrameColorCommand(UICommand):
    color: Color

@dataclass
class SetBackgroundColorCommand(UICommand):
    color: Color

@dataclass
class UnsetBackgroundColorCommand(UICommand):
    color: Color

@dataclass
class SetTextColorCommand(UICommand):
    color: Color

@dataclass
class UnsetTextColorCommand(UICommand):
    color: Color
