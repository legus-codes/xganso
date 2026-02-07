from dataclasses import dataclass
import string

from core.primitives import Color


@dataclass(slots=True, frozen=True)
class InteractionColors:
    normal: Color | None = None
    hovered: Color | None = None
    pressed: Color | None = None
    focused: Color | None = None
    selected: Color | None = None
    disabled: Color | None = None


@dataclass
class FrameDescription:
    width: int
    colors: InteractionColors | None


@dataclass
class LayoutDescription: ...


@dataclass
class HorizontalLayoutDescription(LayoutDescription):
    spacing: int


@dataclass
class VerticalLayoutDescription(LayoutDescription):
    spacing: int


@dataclass
class GridLayoutDescription(LayoutDescription):
    rows: int
    cols: int
    h_spacing: int
    v_spacing: int


@dataclass
class TextStyleDescription:
    font: str
    size: int
    color: InteractionColors | None


class InputFilters:
    NUMBERS = set(string.digits)
    TEXT = set(string.ascii_letters + string.digits + " .-_")
