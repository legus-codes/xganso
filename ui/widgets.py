from typing import List, Optional
import pygame
from ecs_framework.ecs import ECS, ComponentProtocol
from ui.components.data import Trigger, Label, RadioItem, RenderLayer, Variable
from ui.components.formatting import Allignment, TextAllignment, Color, Font
from ui.components.layout import Widget, Parent, Rect, RelativeRect
from ui.components.rendering import Frameable, Highlightable, Labelable, NeedRedraw, Renderable
from ui.components.state import Enabled, Focusable, Hoverable, Pressable, Selectable, Toggleable, Typeable


def _get_default_colors(**kwargs) -> Color:
    return Color(text=pygame.Color(kwargs.get('text', 'beige')),
                   background=pygame.Color(kwargs.get('background', 'black')),
                   hover=pygame.Color(kwargs.get('hover', 'red')),
                   press=pygame.Color(kwargs.get('press', 'darkgray')),
                   focus=pygame.Color(kwargs.get('focus', 'green')),
                   select=pygame.Color(kwargs.get('select', 'blue')),
                   frame=pygame.Color(kwargs.get('frame', 'yellow')))


def _get_default_font() -> Font:
    return Font(pygame.font.SysFont('couriernew', 16))


def _get_char_range(start_char: str, end_char: str) -> List[str]:
    return [chr(char) for char in range(ord(start_char), ord(end_char) + 1)]


def _get_int_input() -> Typeable:
    return Typeable(_get_char_range('0', '9'))


def _get_text_input() -> Typeable:
    text_input = _get_int_input()
    text_input.accepted_chars.extend(_get_char_range('a', 'z'))
    text_input.accepted_chars.extend(_get_char_range('A', 'Z'))
    text_input.accepted_chars.extend([' ', '.', '-', '_'])
    return text_input


def _create_base_widget(world: ECS, layer: int, rect: pygame.Rect, parent: Optional[int], **kwargs) -> int:
    entity = world.create_entity()
    world.add_component(entity, Widget())
    if parent is None:
        world.add_component(entity, Rect(rect))
    else:
        world.add_component(entity, Parent(parent))
        world.add_component(entity, RelativeRect(rect))
    world.add_component(entity, _get_default_colors(**kwargs))
    world.add_component(entity, _get_default_font())
    world.add_component(entity, Enabled())
    world.add_component(entity, RenderLayer(layer))
    world.add_component(entity, Renderable())
    world.add_component(entity, NeedRedraw())
    return entity


def create_text(world: ECS, text: str, rect: pygame.Rect, parent: Optional[int] = None) -> int:
    entity = _create_base_widget(world, 10, rect, parent)
    world.add_component(entity, Labelable())

    world.add_component(entity, Label(text))
    world.add_component(entity, TextAllignment(Allignment.center))
    return entity


def create_text_input(world: ECS, label: str, text: str, rect: pygame.Rect, parent: Optional[int] = None) -> int:
    entity = _create_base_widget(world, 10, rect, parent)

    world.add_component(entity, Hoverable())
    world.add_component(entity, Focusable())
    world.add_component(entity, _get_text_input())
    world.add_component(entity, Highlightable())
    world.add_component(entity, Labelable())

    world.add_component(entity, Label(label))
    world.add_component(entity, TextAllignment(Allignment.left))
    world.add_component(entity, Variable(text, str))
    return entity


def create_int_text_input(world: ECS, label: str, value: str, rect: pygame.Rect, parent: Optional[int] = None) -> int:
    entity = _create_base_widget(world, 10, rect, parent)

    world.add_component(entity, Hoverable())
    world.add_component(entity, Focusable())
    world.add_component(entity, _get_int_input())
    world.add_component(entity, Highlightable())
    world.add_component(entity, Labelable())


    world.add_component(entity, Label(label))
    world.add_component(entity, TextAllignment(Allignment.left))
    world.add_component(entity, Variable(value, int))
    return entity


def create_button(world: ECS, label: str, rect: pygame.Rect, trigger: ComponentProtocol, parent: Optional[int] = None) -> int:
    entity = _create_base_widget(world, 10, rect, parent)

    world.add_component(entity, Hoverable())
    world.add_component(entity, Pressable())
    world.add_component(entity, Highlightable())
    world.add_component(entity, Labelable())

    if trigger:
        world.add_component(entity, Trigger(trigger))
    
    world.add_component(entity, Label(label))
    world.add_component(entity, TextAllignment(Allignment.center))
    return entity


def create_radio_button(world: ECS, label: str, radio_group: str, rect: pygame.Rect, parent: Optional[int] = None, trigger: Optional[ComponentProtocol] = None) -> int:
    entity = create_button(world, label, rect, trigger, parent)
    world.add_component(entity, Selectable())
    world.add_component(entity, RadioItem(radio_group))
    return entity


def create_toggle(world: ECS, label: str, rect: pygame.Rect, parent: Optional[int] = None, trigger: Optional[ComponentProtocol] = None) -> int:
    entity = create_button(world, label, rect, trigger, parent)
    world.add_component(entity, Toggleable())
    return entity


def create_panel(world: ECS, rect: pygame.Rect, frame_color: str = 'yellow', parent: Optional[int] = None) -> int:
    entity = _create_base_widget(world, 0, rect, parent, **{'frame': frame_color})
    world.add_component(entity, Frameable())
    world.add_component(entity, Highlightable())

    return entity
