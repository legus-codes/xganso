from dataclasses import dataclass
import string

from core.primitives import Color, IVec2


@dataclass
class ItemSizeDescription:
    width: int
    height: int


@dataclass
class LayoutDescription: ...


@dataclass
class HorizontalLayoutDescription(LayoutDescription):
    spacing: int
    padding: IVec2
    item_size: ItemSizeDescription | None = None


@dataclass
class VerticalLayoutDescription(LayoutDescription):
    spacing: int
    padding: IVec2
    item_size: ItemSizeDescription | None = None


@dataclass
class GridLayoutDescription(LayoutDescription):
    rows: int
    cols: int
    spacing: IVec2
    padding: IVec2
    item_size: ItemSizeDescription | None = None


@dataclass
class TextStyleDescription:
    font: str
    size: int
    color: Color | None


class InputFilters:
    NUMBERS = set(string.digits)
    TEXT = set(string.ascii_letters + string.digits + " .-_")
