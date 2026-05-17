from dataclasses import dataclass, field
from typing import Iterable

from core.primitives import Color, ColorStack, Vec2
from omniecs.types import Bundle, Component, EntityId
from ui.components.command import UICommand
from ui.components.content import Text, InputValue
from ui.components.style import Background, BlinkingEffect, Frame, TextStyle
from ui.components.layout import FixedItemSize, HorizontalAlignment, GridLayout, HorizontalLayout, RenderLayer, Spacing, TextAlignment, Transform, Parent, VerticalAlignment, VerticalLayout
from ui.components.rendering import Dirty
from ui.components.behavior import Enabled, Focusable, Hoverable, Pressable, Pressable, Selectable, Selected, SelectionGroup, Toggleable, Toggled, Trigger, InputFilter
from ui.types import GridLayoutDescription, HorizontalLayoutDescription, LayoutDescription, TextStyleDescription, VerticalLayoutDescription


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
        yield TextStyle(self.style.font, self.style.size, ColorStack(self.style.color))
        yield TextAlignment(self.horizontal_alignment, self.vertical_alignment)
        yield Spacing(self.horizontal_spacing, self.vertical_spacing)


@dataclass
class RectTransformBundle(Bundle):
    size: Vec2
    position: Vec2 = field(default_factory=Vec2)
    parent: EntityId | None = None
    layer: int = 0

    def components(self) -> Iterable[Component]:
        yield Transform(self.position, self.size)
        yield RenderLayer(self.layer)
        if self.parent is not None:
            yield Parent(self.parent)


@dataclass
class PanelLayoutBundle(Bundle):
    layout: LayoutDescription | None = None

    def components(self) -> Iterable[Component]:
        if isinstance(self.layout, HorizontalLayoutDescription):
            yield HorizontalLayout(self.layout.spacing, self.layout.padding)
        elif isinstance(self.layout, VerticalLayoutDescription):
            yield VerticalLayout(self.layout.spacing, self.layout.padding)
        elif isinstance(self.layout, GridLayoutDescription):
            yield GridLayout(self.layout.rows, self.layout.rows, self.layout.spacing, self.layout.padding)
        if self.layout is not None and self.layout.item_size is not None:
            yield FixedItemSize(self.layout.item_size.width, self.layout.item_size.height)


@dataclass
class SurfaceBundle(Bundle):
    background_color: Color
    frame_color: Color | None = None
    frame_width: int = 0

    def components(self) -> Iterable[Component]:
        if self.background_color is not None:
            yield Background(ColorStack(self.background_color))
        if self.frame_color is not None and self.frame_width > 0:
            yield Frame(ColorStack(self.frame_color), self.frame_width)


@dataclass
class HoverableBundle(Bundle):
    enter: list[UICommand] = field(default_factory=list)
    exit: list[UICommand] = field(default_factory=list)

    def components(self) -> Iterable[Component]:
        yield Hoverable(enter=self.enter, exit=self.exit)


@dataclass
class PressableBundle(Bundle):
    enter: list[UICommand] = field(default_factory=list)
    exit: list[UICommand] = field(default_factory=list)

    def components(self) -> Iterable[Component]:
        yield Pressable(enter=self.enter, exit=self.exit)


@dataclass
class ActivatableBundle(Bundle):
    commands: list[UICommand] = field(default_factory=list)

    def components(self) -> Iterable[Component]:
        yield Trigger(self.commands)


@dataclass
class ToggleableBundle(Bundle):
    enter: list[UICommand] = field(default_factory=list)
    exit: list[UICommand] = field(default_factory=list)
    active: bool = False

    def components(self) -> Iterable[Component]:
        yield Toggleable(enter=self.enter, exit=self.exit)
        if self.active:
            yield Toggled()


@dataclass
class InputBundle(Bundle):
    #TODO: icha said to put character limit because the user is an idiot
    input_value: str
    input_filter: set[str]

    def components(self) -> Iterable[Component]:
        yield Focusable()
        yield BlinkingEffect()
        yield InputValue(self.input_value)
        yield InputFilter(self.input_filter)


@dataclass
class SelectableBundle(Bundle):
    group: str
    enter: list[UICommand] = field(default_factory=list)
    exit: list[UICommand] = field(default_factory=list)
    active: bool = False

    def components(self) -> Iterable[Component]:
        yield SelectionGroup(self.group)
        yield Selectable(enter=self.enter, exit=self.exit)
        if self.active:
            yield Selected()
