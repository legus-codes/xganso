from omniecs.world import World, WorldFactory

from core.primitives import Color
from ui.components.behavior import Selectable, Selected, SelectionGroup
from ui.components.command import SetFrameColorCommand
from ui.events.events import DeselectGroupEvent
from ui.systems.consistency_system import SelectionGroupConsistencyCheckerSystem

def create_world() -> World:
    world = WorldFactory.create_empty_world()
    world.register_system(SelectionGroupConsistencyCheckerSystem())
    return world


def test_one_entity():
    world = create_world()

    entity_id = world.spawn(Selectable(), SelectionGroup(group='group'), Selected())
    world.execute()

    assert world.query_entities(all_of=(Selected,)) == set([entity_id])
    assert world.get_events() == []

def test_one_enabled_entity():
    world = create_world()

    entity_id1 = world.spawn(Selectable(), SelectionGroup(group='group'), Selected())
    entity_id2 = world.spawn(Selectable(), SelectionGroup(group='group'))
    world.execute()

    assert world.query_entities(all_of=(Selected,)) == set([entity_id1])
    assert world.query_entities(none_of=(Selected,)) == set([entity_id2])
    assert world.get_events() == []

def test_multiple_enabled_entities():
    world = create_world()

    entity_id1 = world.spawn(Selectable(), SelectionGroup(group='group'), Selected())
    entity_id2 = world.spawn(Selectable(), SelectionGroup(group='group'), Selected())
    world.execute()

    assert world.query_entities(all_of=(Selected,)) == set([entity_id1, entity_id2])
    assert len(world.get_events()) == 1
    event = world.get_events()[0]
    assert isinstance(event, DeselectGroupEvent)
    assert event.group == 'group'
    assert event.selected == entity_id1

def test_multiple_enabled_entities_with_command():
    world = create_world()

    entity_id1 = world.spawn(Selectable(enter=[SetFrameColorCommand(Color(0, 0, 0))]), SelectionGroup(group='group'), Selected())
    entity_id2 = world.spawn(Selectable(enter=[SetFrameColorCommand(Color(0, 0, 0))]), SelectionGroup(group='group'), Selected())
    world.execute()

    assert world.query_entities(all_of=(Selected, SetFrameColorCommand)) == set([entity_id1])
    assert world.query_entities(all_of=(Selected,), none_of=(SetFrameColorCommand,)) == set([entity_id2])
    assert len(world.get_events()) == 1
    event = world.get_events()[0]
    assert isinstance(event, DeselectGroupEvent)
    assert event.group == 'group'
    assert event.selected == entity_id1

