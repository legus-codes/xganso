from omniecs.world import EntityId, World, WorldFactory

from core.primitives import Color
from ui.components.behavior import Focusable, Focused, Selectable, Selected, SelectionGroup
from ui.components.command import UnsetFrameColorCommand
from ui.components.rendering import Dirty
from ui.events.events import DeselectGroupEvent, LoseFocusEvent
from ui.systems.behaviour_system import UnfocusSystem


def create_world() -> World:
    world = WorldFactory.create_world()
    world.register_system(UnfocusSystem())
    return world

def test_no_event():
    world = create_world()

    entity_id = world.spawn(Focusable(), Focused())
    world.execute()

    assert world.query_entities(all_of=(Focused,), none_of=(Dirty,)) == set([entity_id])

def test_no_focusable():
    world = create_world()

    entity_id = world.spawn(Focused())
    world.push_event(LoseFocusEvent(focused=EntityId(1000)))
    world.execute()

    assert world.query_entities(all_of=(Focused,), none_of=(Dirty,)) == set([entity_id])

def test_unfocus():
    world = create_world()

    entity_id = world.spawn(Focused(), Focusable())
    world.push_event(LoseFocusEvent(focused=EntityId(1000)))
    world.execute()

    assert world.query_entities(all_of=(Dirty,), none_of=(Focused,)) == set([entity_id])

def test_unfocus_with_command():
    world = create_world()

    entity_id = world.spawn(Focused(), Focusable(exit=[UnsetFrameColorCommand(Color(0, 0, 0))]))
    world.push_event(LoseFocusEvent(focused=EntityId(1000)))
    world.execute()

    assert world.query_entities(all_of=(Dirty, UnsetFrameColorCommand), none_of=(Focused,)) == set([entity_id])

def test_unfocus_entity_focused():
    world = create_world()

    entity_id = world.spawn(Focused(), Focusable(exit=[UnsetFrameColorCommand(Color(0, 0, 0))]))
    world.push_event(LoseFocusEvent(focused=entity_id))
    world.execute()

    assert world.query_entities(all_of=(Focused,), none_of=(Dirty,)) == set([entity_id])

def test_another_event():
    world = create_world()

    entity_id = world.spawn(Focused(), Focusable())
    world.push_event(DeselectGroupEvent(group='group2', selected=EntityId(1000)))
    world.execute()

    assert world.query_entities(all_of=(Focused,), none_of=(Dirty,)) == set([entity_id])
