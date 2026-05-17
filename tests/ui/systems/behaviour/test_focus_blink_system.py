from omniecs.world import World, WorldFactory

from core.primitives import Color
from ui.components.behavior import Focusable, Focused
from ui.components.command import SetTextColorCommand
from ui.components.intent import PressIntent
from ui.components.rendering import Dirty
from ui.components.style import BlinkingEffect
from ui.events.events import LoseFocusEvent
from ui.systems.behaviour_system import FocusBlinkSystem, FocusSystem


def create_world() -> World:
    world = WorldFactory.create_world()
    world.register_system(FocusBlinkSystem())
    return world

def test_no_focused():
    world = create_world()

    entity_id = world.spawn(BlinkingEffect())
    world.execute(100)

    assert world.query_entities(none_of=(Dirty,)) == set([entity_id])
    blinking: BlinkingEffect = world.get_component(entity_id, BlinkingEffect)
    assert blinking.timer == 0
    assert blinking.visible

def test_increase_timer():
    world = create_world()

    entity_id = world.spawn(BlinkingEffect(), Focused())
    world.execute(100)

    assert world.query_entities(none_of=(Dirty,)) == set([entity_id])
    blinking: BlinkingEffect = world.get_component(entity_id, BlinkingEffect)
    assert blinking.timer == 100
    assert blinking.visible

def test_turn_not_visible():
    world = create_world()

    entity_id = world.spawn(BlinkingEffect(), Focused())
    world.execute(501)

    assert world.query_entities(all_of=(Dirty,)) == set([entity_id])
    blinking: BlinkingEffect = world.get_component(entity_id, BlinkingEffect)
    assert blinking.timer == 1
    assert not blinking.visible

def test_turn_visible():
    world = create_world()

    entity_id = world.spawn(BlinkingEffect(visible=False), Focused())
    world.execute(750)

    assert world.query_entities(all_of=(Dirty,)) == set([entity_id])
    blinking: BlinkingEffect = world.get_component(entity_id, BlinkingEffect)
    assert blinking.timer == 250
    assert blinking.visible
