from omniecs.world import EntityId, World, WorldFactory

from core.primitives import Color
from ui.components.behavior import Selectable, Selected, SelectionGroup
from ui.components.command import UnsetFrameColorCommand
from ui.events.events import DeselectGroupEvent, LoseFocusEvent
from ui.systems.behaviour_system import DeselectSystem


def create_world() -> World:
    world = WorldFactory.create_world()
    world.register_system(DeselectSystem())
    return world

def test_no_event():
    world = create_world()

    entity_id = world.spawn(Selectable(), Selected(), SelectionGroup(group='group'))
    world.execute()

    assert world.query_entities(all_of=(Selected,)) == set([entity_id])

def test_no_selectable():
    world = create_world()

    entity_id = world.spawn(Selected(), SelectionGroup(group='group'))
    world.push_event(DeselectGroupEvent(group='group', selected=EntityId(1000)))
    world.execute()

    assert world.query_entities(all_of=(Selected,)) == set([entity_id])

def test_no_selection_group():
    world = create_world()

    entity_id = world.spawn(Selected(), Selectable())
    world.push_event(DeselectGroupEvent(group='group', selected=EntityId(1000)))
    world.execute()

    assert world.query_entities(all_of=(Selected,)) == set([entity_id])

def test_deselect():
    world = create_world()

    entity_id = world.spawn(Selected(), Selectable(), SelectionGroup(group='group'))
    world.push_event(DeselectGroupEvent(group='group', selected=EntityId(1000)))
    world.execute()

    assert world.query_entities(none_of=(Selected,)) == set([entity_id])

def test_deselect_with_command():
    world = create_world()

    entity_id = world.spawn(Selected(), Selectable(exit=[UnsetFrameColorCommand(Color(0, 0, 0))]), SelectionGroup(group='group'))
    world.push_event(DeselectGroupEvent(group='group', selected=EntityId(1000)))
    world.execute()

    assert world.query_entities(all_of=(UnsetFrameColorCommand,), none_of=(Selected,)) == set([entity_id])

def test_deselect_entity_selected():
    world = create_world()

    entity_id = world.spawn(Selected(), Selectable(), SelectionGroup(group='group'))
    world.push_event(DeselectGroupEvent(group='group', selected=entity_id))
    world.execute()

    assert world.query_entities(all_of=(Selected,)) == set([entity_id])

def test_deselect_another_group():
    world = create_world()

    entity_id = world.spawn(Selected(), Selectable(), SelectionGroup(group='group'))
    world.push_event(DeselectGroupEvent(group='group2', selected=EntityId(1000)))
    world.execute()

    assert world.query_entities(all_of=(Selected,)) == set([entity_id])

def test_another_event():
    world = create_world()

    entity_id = world.spawn(Selected(), Selectable(), SelectionGroup(group='group'))
    world.push_event(LoseFocusEvent(focused=entity_id))
    world.execute()

    assert world.query_entities(all_of=(Selected,)) == set([entity_id])
