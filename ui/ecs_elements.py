import pygame
from ecs_framework.ecs import ECS
from ui.ui_components import UICallback, UIColor, UIElement, UIFont, UIInt, UILabel, UIPadding, UIRect, UIState, UIString, UIText


def _get_default_colors() -> UIColor:
    return UIColor(pygame.Color('beige'),
                   pygame.Color('black'),
                   pygame.Color('red'),
                   pygame.Color('darkgray'),
                   pygame.Color('blue'))


def _get_default_font() -> UIFont:
    return UIFont(pygame.font.SysFont('Arial', 16))


def create_text(ecs: ECS, text: str, rect: pygame.Rect) -> None:
    entity = ecs.create_entity()
    ecs.add_component(entity, UIElement())
    ecs.add_component(entity, UIRect(rect))
    ecs.add_component(entity, _get_default_colors())
    ecs.add_component(entity, _get_default_font())
    ecs.add_component(entity, UIState(True))

    ecs.add_component(entity, UIPadding(left=7))
    ecs.add_component(entity, UIText(text))


def create_button(ecs: ECS, label: str, rect: pygame.Rect) -> None:
    entity = ecs.create_entity()
    ecs.add_component(entity, UIElement())
    ecs.add_component(entity, UIRect(rect))
    ecs.add_component(entity, _get_default_colors())
    ecs.add_component(entity, _get_default_font())
    ecs.add_component(entity, UIState(True))

    ecs.add_component(entity, UICallback(None))
    ecs.add_component(entity, UILabel(label))


def create_text_input(ecs: ECS, label: str, rect: pygame.Rect) -> None:
    entity = ecs.create_entity()
    ecs.add_component(entity, UIElement())
    ecs.add_component(entity, UIRect(rect))
    ecs.add_component(entity, _get_default_colors())
    ecs.add_component(entity, _get_default_font())
    ecs.add_component(entity, UIState(True))

    ecs.add_component(entity, UILabel(label))
    ecs.add_component(entity, UIString('text'))


def create_int_text_input(ecs: ECS, label: str, rect: pygame.Rect) -> None:
    entity = ecs.create_entity()
    ecs.add_component(entity, UIElement())
    ecs.add_component(entity, UIRect(rect))
    ecs.add_component(entity, _get_default_colors())
    ecs.add_component(entity, _get_default_font())
    ecs.add_component(entity, UIState(True))

    ecs.add_component(entity, UILabel(label))
    ecs.add_component(entity, UIInt(0))


def create_radio_button(ecs: ECS, label: str, rect: pygame.Rect) -> None:
    entity = ecs.create_entity()
    ecs.add_component(entity, UIElement())
    ecs.add_component(entity, UIRect(rect))
    ecs.add_component(entity, _get_default_colors())
    ecs.add_component(entity, _get_default_font())
    ecs.add_component(entity, UIState(True))

    ecs.add_component(entity, UILabel(label))


def create_toggle(ecs: ECS, label: str, rect: pygame.Rect) -> None:
    entity = ecs.create_entity()
    ecs.add_component(entity, UIElement())
    ecs.add_component(entity, UIRect(rect))
    ecs.add_component(entity, _get_default_colors())
    ecs.add_component(entity, _get_default_font())
    ecs.add_component(entity, UIState(True))
    
    ecs.add_component(entity, UILabel(label))
