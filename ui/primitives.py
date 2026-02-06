from dataclasses import dataclass


@dataclass(slots=True)
class Color:
    r: int
    g: int
    b: int
    a: int = 255


@dataclass(slots=True, frozen=True)
class InteractionColors:
    normal: Color | None = None
    hovered: Color | None = None
    pressed: Color | None = None
    focused: Color | None = None
    selected: Color | None = None
    disabled: Color | None = None


@dataclass(slots=True)
class Vec2:
    x: float = 0
    y: float = 0


@dataclass(slots=True)
class IVec2:
    x: int = 0
    y: int = 0


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

