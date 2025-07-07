import pygame
from ecs_framework.ecs import ECS
from ui.ui_components import Allignment, UICallback, UIColor, UIElement, UIEnabled, UIFocusable, UIFont, UIHoverable, UIInt, UILabel, UIPadding, UIPressable, UIRadioGroup, UIRect, UISelectable, UIString, UIText, UIToggleable


def _get_default_colors() -> UIColor:
    return UIColor(text=pygame.Color('beige'),
                   background=pygame.Color('black'),
                   hover=pygame.Color('red'),
                   press=pygame.Color('darkgray'),
                   focus=pygame.Color('green'),
                   select=pygame.Color('blue'))


def _get_default_font() -> UIFont:
    return UIFont(pygame.font.SysFont('Arial', 16))


def create_text(ecs: ECS, text: str, rect: pygame.Rect) -> None:
    entity = ecs.create_entity()
    ecs.add_component(entity, UIElement())
    ecs.add_component(entity, UIRect(rect))
    ecs.add_component(entity, _get_default_colors())
    ecs.add_component(entity, _get_default_font())
    ecs.add_component(entity, UIEnabled())

    ecs.add_component(entity, UIPadding(left=7))
    ecs.add_component(entity, UIText(text))


def create_button(ecs: ECS, label: str, rect: pygame.Rect) -> None:
    entity = ecs.create_entity()
    ecs.add_component(entity, UIElement())
    ecs.add_component(entity, UIRect(rect))
    ecs.add_component(entity, _get_default_colors())
    ecs.add_component(entity, _get_default_font())
    ecs.add_component(entity, UIEnabled())
    ecs.add_component(entity, UIHoverable())
    ecs.add_component(entity, UIPressable())

    ecs.add_component(entity, UICallback(lambda: print('ecs button')))
    ecs.add_component(entity, UILabel(label, Allignment.center))


def create_text_input(ecs: ECS, label: str, rect: pygame.Rect) -> None:
    entity = ecs.create_entity()
    ecs.add_component(entity, UIElement())
    ecs.add_component(entity, UIRect(rect))
    ecs.add_component(entity, _get_default_colors())
    ecs.add_component(entity, _get_default_font())
    ecs.add_component(entity, UIEnabled())
    ecs.add_component(entity, UIHoverable())
    ecs.add_component(entity, UIFocusable())

    ecs.add_component(entity, UILabel(label, Allignment.left))
    ecs.add_component(entity, UIString('text'))


def create_int_text_input(ecs: ECS, label: str, rect: pygame.Rect) -> None:
    entity = ecs.create_entity()
    ecs.add_component(entity, UIElement())
    ecs.add_component(entity, UIRect(rect))
    ecs.add_component(entity, _get_default_colors())
    ecs.add_component(entity, _get_default_font())
    ecs.add_component(entity, UIEnabled())
    ecs.add_component(entity, UIHoverable())
    ecs.add_component(entity, UIFocusable())

    ecs.add_component(entity, UILabel(label, Allignment.left))
    ecs.add_component(entity, UIInt(0))


def create_radio_button(ecs: ECS, label: str, rect: pygame.Rect) -> None:
    entity = ecs.create_entity()
    ecs.add_component(entity, UIElement())
    ecs.add_component(entity, UIRect(rect))
    ecs.add_component(entity, _get_default_colors())
    ecs.add_component(entity, _get_default_font())
    ecs.add_component(entity, UIEnabled())
    ecs.add_component(entity, UIHoverable())
    ecs.add_component(entity, UISelectable())

    ecs.add_component(entity, UILabel(label, Allignment.center))
    ecs.add_component(entity, UIRadioGroup('test'))


def create_toggle(ecs: ECS, label: str, rect: pygame.Rect) -> None:
    entity = ecs.create_entity()
    ecs.add_component(entity, UIElement())
    ecs.add_component(entity, UIRect(rect))
    ecs.add_component(entity, _get_default_colors())
    ecs.add_component(entity, _get_default_font())
    ecs.add_component(entity, UIEnabled())
    ecs.add_component(entity, UIHoverable())
    ecs.add_component(entity, UIToggleable())
    
    ecs.add_component(entity, UILabel(label, Allignment.center))
