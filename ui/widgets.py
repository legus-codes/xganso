import pygame

from dataclasses import dataclass, field
from typing import Callable, Iterable, Optional, Set

from ecs_framework.ecs import ECS, Bundle, ComponentProtocol
from ui.components.content import Text
from ui.components.style import Background, Frame, TextStyle
from ui.components.layout import TextAlignmentEnum, GridLayout, HorizontalLayout, RenderLayer, TextAlignment, Transform, Parent, VerticalLayout
from ui.components.rendering import Dirty
from ui.components.behavior import Enabled, Focusable, Hoverable, Pressable, Selectable, Toggleable, Toggled, Trigger, Typeable
from ui.primitives import Color, FrameDescription, GridLayoutDescription, HorizontalLayoutDescription, InteractionColors, LayoutDescription, TextStyleDescription, Vec2, VerticalLayoutDescription


@dataclass
class WidgetCoreBundle(Bundle):
    enabled: bool = True

    def components(self) -> Iterable[ComponentProtocol]:
        if self.enabled:
            yield Enabled()
        yield Dirty()


@dataclass
class TextVisualBundle(Bundle):
    text: str
    style: TextStyleDescription
    alignment: TextAlignmentEnum = TextAlignmentEnum.left

    def components(self) -> Iterable[ComponentProtocol]:
        yield Text(self.text)
        yield TextStyle(self.style.font, self.style.size, self.style.color)
        yield TextAlignment(self.alignment)


@dataclass
class RectTransformBundle(Bundle):
    size: Vec2
    position: Vec2 = field(default_factory=Vec2)
    parent: int | None = None
    layer: int = 0

    def components(self) -> Iterable[ComponentProtocol]:
        yield Transform(self.size, self.position)
        yield RenderLayer(self.layer)
        if self.parent is not None:
            yield Parent(self.parent)


@dataclass
class PanelLayoutBundle(Bundle):
    layout: LayoutDescription | None = None

    def components(self) -> Iterable[ComponentProtocol]:
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

    def components(self) -> Iterable[ComponentProtocol]:
        if self.background_colors is not None:
            yield Background(self.background_colors)
        if self.frame is not None and self.frame.width > 0:
            yield Frame(self.frame.width, self.frame.colors)


@dataclass
class InteractableBundle(Bundle):
    trigger: ComponentProtocol

    def components(self) -> Iterable[ComponentProtocol]:
        yield Hoverable()
        yield Pressable()
        yield Trigger(self.trigger)


@dataclass
class ToggleableBundle(Bundle):
    active: bool = False

    def components(self) -> Iterable[ComponentProtocol]:
        yield Toggleable()
        if self.active:
            yield Toggled()


@dataclass
class PanelBundle(Bundle):
    core: WidgetCoreBundle
    transform: RectTransformBundle
    layout: PanelLayoutBundle
    decoration: SurfaceBundle
    
    def components(self) -> Iterable[ComponentProtocol]:
        yield from self.core.components()
        yield from self.transform.components()
        yield from self.layout.components()
        yield from self.decoration.components()


@dataclass
class TextBundle(Bundle):
    core: WidgetCoreBundle
    text: TextVisualBundle
    transform: RectTransformBundle
    decoration: SurfaceBundle
    
    def components(self) -> Iterable[ComponentProtocol]:
        yield from self.core.components()
        yield from self.text.components()
        yield from self.transform.components()
        yield from self.decoration.components()


@dataclass
class ButtonBundle(Bundle):
    core: WidgetCoreBundle
    text: TextVisualBundle
    transform: RectTransformBundle
    decoration: SurfaceBundle
    interactable: InteractableBundle
    
    def components(self) -> Iterable[ComponentProtocol]:
        yield from self.core.components()
        yield from self.text.components()
        yield from self.transform.components()
        yield from self.decoration.components()
        yield from self.interactable.components()


@dataclass
class ToggleBundle(Bundle):
    core: WidgetCoreBundle
    text: TextVisualBundle
    transform: RectTransformBundle
    decoration: SurfaceBundle
    interactable: InteractableBundle
    toggleable: ToggleableBundle
    
    def components(self) -> Iterable[ComponentProtocol]:
        yield from self.core.components()
        yield from self.text.components()
        yield from self.transform.components()
        yield from self.decoration.components()
        yield from self.interactable.components()
        yield from self.toggleable.components()


# def _get_default_colors() -> StateColor:
#     return StateColor(background=Color(0, 0, 0, 255),
#                       hover=Color(255, 0, 0, 255),
#                       press=Color(169, 169, 169, 255),
#                       focus=Color(0, 255, 0, 255),
#                       select=Color(0, 0, 255, 255),
#                       frame=Color(255, 255, 0, 255))
# # text=Color(245, 245, 220, 255),

# def _get_char_range(start_char: str, end_char: str) -> Set[str]:
#     return set([chr(char) for char in range(ord(start_char), ord(end_char) + 1)])


# def _get_accepted_numbers() -> Set[str]:
#     return _get_char_range('0', '9')


# def _get_accepted_chars() -> Set[str]:
#     return _get_char_range('0', '9').union(_get_char_range('a', 'z')).union(_get_char_range('A', 'Z')).union(set([' ', '.', '-', '_']))


# def _get_int_input() -> Typeable:
#     return Typeable(_get_accepted_numbers())


# def _get_text_input() -> Typeable:
#     return Typeable(_get_accepted_chars())


# def _create_base_widget(world: ECS, layer: int, position: Vec2, size: Vec2, parent: int | None) -> int:
#     entity = world.create_entity()
#     world.add_component(entity, Parent(parent))
#     world.add_component(entity, Transform(position, size))
#     world.add_component(entity, RenderLayer(layer))
#     world.add_component(entity, Enabled())
#     world.add_component(entity, Dirty())
#     return entity


# def create_text(world: ECS, text: str, rect: pygame.Rect, parent: Optional[int] = None) -> int:
#     entity = _create_base_widget(world, 10, rect, parent)
#     world.add_component(entity, Textable())

#     world.add_component(entity, Text(text, allignment=TextAllignment.center))
#     return entity


# def create_text_input(world: ECS, label: str, text: str, rect: pygame.Rect, parent: Optional[int] = None) -> int:
#     entity = _create_base_widget(world, 10, rect, parent)

#     world.add_component(entity, Hoverable())
#     world.add_component(entity, Focusable())
#     world.add_component(entity, _get_text_input())
#     world.add_component(entity, Highlightable())
#     world.add_component(entity, Textable())

#     world.add_component(entity, Label(label))
#     world.add_component(entity, TextAllignment(Allignment.left))
#     world.add_component(entity, Variable(text, str))
#     return entity


# def create_int_text_input(world: ECS, label: str, value: str, rect: pygame.Rect, parent: Optional[int] = None) -> int:
#     entity = _create_base_widget(world, 10, rect, parent)

#     world.add_component(entity, Hoverable())
#     world.add_component(entity, Focusable())
#     world.add_component(entity, _get_int_input())
#     world.add_component(entity, Highlightable())
#     world.add_component(entity, Textable())


#     world.add_component(entity, Label(label))
#     world.add_component(entity, TextAllignment(Allignment.left))
#     world.add_component(entity, Variable(value, int))
#     return entity


# def create_button(world: ECS, label: str, rect: pygame.Rect, trigger: ComponentProtocol, parent: Optional[int] = None) -> int:
#     entity = _create_base_widget(world, 10, rect, parent)

#     world.add_component(entity, Hoverable())
#     world.add_component(entity, Pressable())
#     world.add_component(entity, Highlightable())
#     world.add_component(entity, Textable())

#     if trigger:
#         world.add_component(entity, Trigger(trigger))
    
#     world.add_component(entity, Label(label))
#     world.add_component(entity, TextAllignment(Allignment.center))
#     return entity


# def create_radio_button(world: ECS, label: str, radio_group: str, rect: pygame.Rect, parent: Optional[int] = None, trigger: Optional[ComponentProtocol] = None) -> int:
#     entity = create_button(world, label, rect, trigger, parent)
#     world.add_component(entity, Selectable())
#     world.add_component(entity, RadioItem(radio_group))
#     return entity


# def create_toggle(world: ECS, label: str, rect: pygame.Rect, parent: Optional[int] = None, trigger: Optional[ComponentProtocol] = None) -> int:
#     entity = create_button(world, label, rect, trigger, parent)
#     world.add_component(entity, Toggleable())
#     return entity


# def create_panel(world: ECS, rect: pygame.Rect, frame_color: str = 'yellow', parent: Optional[int] = None) -> int:
#     entity = _create_base_widget(world, 0, rect, parent, **{'frame': frame_color})
#     world.add_component(entity, Frameable())
#     world.add_component(entity, Highlightable())

#     return entity


# # def create_list


