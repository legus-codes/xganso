from dataclasses import dataclass, field
from typing import Iterable

from core.primitives import Vec2
from omniecs.types import Bundle, Component
from ui.components.content import Text, InputValue
from ui.components.style import Background, Frame, TextStyle
from ui.components.layout import HorizontalAlignment, GridLayout, HorizontalLayout, RenderLayer, Spacing, TextAlignment, Transform, Parent, VerticalAlignment, VerticalLayout
from ui.components.rendering import Dirty
from ui.components.behavior import Enabled, Focusable, Hoverable, Pressable, Selectable, Selected, SelectionGroup, Toggleable, Toggled, Trigger, InputFilter
from ui.types import FrameDescription, GridLayoutDescription, HorizontalLayoutDescription, InteractionColors, LayoutDescription, TextStyleDescription, VerticalLayoutDescription


@dataclass
class WidgetCoreBundle(Bundle):
    enabled: bool = True

    def components(self) -> Iterable[Component]:
        if self.enabled:
            yield Enabled()
        yield Dirty()


@dataclass
class TextVisualBundle(Bundle):
    text: str
    style: TextStyleDescription
    horizontal_alignment: HorizontalAlignment = HorizontalAlignment.left
    vertical_alignment: HorizontalAlignment = VerticalAlignment.top
    horizontal_spacing: int = 0
    vertical_spacing: int = 0

    def components(self) -> Iterable[Component]:
        yield Text(self.text)
        yield TextStyle(self.style.font, self.style.size, self.style.color)
        yield TextAlignment(self.horizontal_alignment, self.vertical_alignment)
        yield Spacing(self.horizontal_spacing, self.vertical_spacing)


@dataclass
class RectTransformBundle(Bundle):
    size: Vec2
    position: Vec2 = field(default_factory=Vec2)
    parent: int | None = None
    layer: int = 0

    def components(self) -> Iterable[Component]:
        yield Transform(self.size, self.position)
        yield RenderLayer(self.layer)
        if self.parent is not None:
            yield Parent(self.parent)


@dataclass
class PanelLayoutBundle(Bundle):
    layout: LayoutDescription | None = None

    def components(self) -> Iterable[Component]:
        if isinstance(self.layout, HorizontalLayoutDescription):
            yield HorizontalLayout(self.layout.spacing)
        elif isinstance(self.layout, VerticalLayoutDescription):
            yield VerticalLayout(self.layout.spacing)
        elif isinstance(self.layout, GridLayoutDescription):
            yield GridLayout(self.layout.rows, self.layout.rows, self.layout.h_spacing, self.layout.v_spacing)


@dataclass
class SurfaceBundle(Bundle):
    background_colors: InteractionColors | None = None
    frame: FrameDescription | None = None

    def components(self) -> Iterable[Component]:
        if self.background_colors is not None:
            yield Background(self.background_colors)
        if self.frame is not None and self.frame.width > 0:
            yield Frame(self.frame.colors, self.frame.width)


@dataclass
class PointerBundle(Bundle):

    def components(self) -> Iterable[Component]:
        yield Hoverable()
        yield Pressable()


@dataclass
class ActivatableBundle(Bundle):
    trigger: Component

    def components(self) -> Iterable[Component]:
        yield Trigger(self.trigger)


@dataclass
class ToggleableBundle(Bundle):
    active: bool = False

    def components(self) -> Iterable[Component]:
        yield Toggleable()
        if self.active:
            yield Toggled()


@dataclass
class InputBundle(Bundle):
    input_value: str
    input_filter: set[str]

    def components(self) -> Iterable[Component]:
        yield Focusable()
        yield InputValue(self.input_value)
        yield InputFilter(self.input_filter)


@dataclass
class SelectableBundle(Bundle):
    radio_group: str
    active: bool = False

    def components(self) -> Iterable[Component]:
        yield SelectionGroup(self.radio_group)
        yield Selectable()
        if self.active:
            yield Selected()
