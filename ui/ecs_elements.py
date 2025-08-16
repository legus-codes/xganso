from typing import Callable, List, Optional
import pygame
from ecs_framework.ecs import ECS
from ui.ui_components import Allignment, UICallback, UIColor, UIElement, UIEnabled, UIFocusable, UIFont, UIForceRedraw, UIFrameable, UIHighlightable, UIHoverable, UILabel, UILabelable, UINeedRedraw, UIParent, UIPressable, UIRadioGroup, UIRect, UIRelativeRect, UIRenderLayer, UIRenderable, UISelectable, UIToggleable, UITypeable, UIVariable


def _get_default_colors(**kwargs) -> UIColor:
    return UIColor(text=pygame.Color(kwargs.get('text', 'beige')),
                   background=pygame.Color(kwargs.get('background', 'black')),
                   hover=pygame.Color(kwargs.get('hover', 'red')),
                   press=pygame.Color(kwargs.get('press', 'darkgray')),
                   focus=pygame.Color(kwargs.get('focus', 'green')),
                   select=pygame.Color(kwargs.get('select', 'blue')),
                   frame=pygame.Color(kwargs.get('frame', 'yellow')))


def _get_default_font() -> UIFont:
    return UIFont(pygame.font.SysFont('couriernew', 16))


def _get_char_range(start_char: str, end_char: str) -> List[str]:
    return [chr(char) for char in range(ord(start_char), ord(end_char) + 1)]


def _get_int_input() -> UITypeable:
    return UITypeable(_get_char_range('0', '9'))


def _get_text_input() -> UITypeable:
    text_input = _get_int_input()
    text_input.accepted_chars.extend(_get_char_range('a', 'z'))
    text_input.accepted_chars.extend(_get_char_range('A', 'Z'))
    text_input.accepted_chars.extend([' ', '.', '-', '_'])
    return text_input


def _create_base_widget(ecs: ECS, layer: int, rect: pygame.Rect, parent: Optional[int], **kwargs) -> int:
    entity = ecs.create_entity()
    ecs.add_component(entity, UIElement())
    if parent is None:
        ecs.add_component(entity, UIRect(rect))
    else:
        ecs.add_component(entity, UIParent(parent))
        ecs.add_component(entity, UIRelativeRect(rect))
    ecs.add_component(entity, _get_default_colors(**kwargs))
    ecs.add_component(entity, _get_default_font())
    ecs.add_component(entity, UIEnabled())
    ecs.add_component(entity, UIRenderLayer(layer))
    ecs.add_component(entity, UIRenderable())
    ecs.add_component(entity, UINeedRedraw())
    return entity


def create_text(ecs: ECS, text: str, rect: pygame.Rect, parent: Optional[int] = None) -> int:
    entity = _create_base_widget(ecs, 10, rect, parent)
    ecs.add_component(entity, UILabelable())

    ecs.add_component(entity, UILabel(text, Allignment.center))
    return entity


def create_button(ecs: ECS, label: str, rect: pygame.Rect, callback: Callable, parent: Optional[int] = None) -> int:
    entity = _create_base_widget(ecs, 10, rect, parent)

    ecs.add_component(entity, UIHoverable())
    ecs.add_component(entity, UIPressable())
    ecs.add_component(entity, UIHighlightable())
    ecs.add_component(entity, UILabelable())

    ecs.add_component(entity, UICallback(callback))
    ecs.add_component(entity, UILabel(label, Allignment.center))
    return entity


def create_text_input(ecs: ECS, label: str, text: str, rect: pygame.Rect, parent: Optional[int] = None) -> int:
    entity = _create_base_widget(ecs, 10, rect, parent)

    ecs.add_component(entity, UIHoverable())
    ecs.add_component(entity, UIFocusable())
    ecs.add_component(entity, _get_text_input())
    ecs.add_component(entity, UIHighlightable())
    ecs.add_component(entity, UILabelable())

    ecs.add_component(entity, UILabel(label, Allignment.left))
    ecs.add_component(entity, UIVariable(text, str))
    return entity


def create_int_text_input(ecs: ECS, label: str, value: str, rect: pygame.Rect, parent: Optional[int] = None) -> int:
    entity = _create_base_widget(ecs, 10, rect, parent)

    ecs.add_component(entity, UIHoverable())
    ecs.add_component(entity, UIFocusable())
    ecs.add_component(entity, _get_int_input())
    ecs.add_component(entity, UIHighlightable())
    ecs.add_component(entity, UILabelable())

    ecs.add_component(entity, UILabel(label, Allignment.left))
    ecs.add_component(entity, UIVariable(value, int))
    return entity


def create_radio_button(ecs: ECS, label: str, radio_group: str, rect: pygame.Rect, parent: Optional[int] = None) -> int:
    entity = _create_base_widget(ecs, 10, rect, parent)

    ecs.add_component(entity, UIHoverable())
    ecs.add_component(entity, UISelectable())
    ecs.add_component(entity, UIHighlightable())
    ecs.add_component(entity, UILabelable())

    ecs.add_component(entity, UILabel(label, Allignment.center))
    ecs.add_component(entity, UIRadioGroup(radio_group))
    return entity


def create_toggle(ecs: ECS, label: str, rect: pygame.Rect, parent: Optional[int] = None) -> int:
    entity = _create_base_widget(ecs, 10, rect, parent)

    ecs.add_component(entity, UIHoverable())
    ecs.add_component(entity, UIToggleable())
    ecs.add_component(entity, UIHighlightable())
    ecs.add_component(entity, UILabelable())
    
    ecs.add_component(entity, UILabel(label, Allignment.center))
    return entity


def create_panel(ecs: ECS, rect: pygame.Rect, frame_color: str = 'yellow', parent: Optional[int] = None) -> int:
    entity = _create_base_widget(ecs, 0, rect, parent, **{'frame': frame_color})
    ecs.add_component(entity, UIFrameable())
    ecs.add_component(entity, UIHighlightable())

    return entity
