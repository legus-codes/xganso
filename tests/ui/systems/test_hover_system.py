# pointer = self.world.get_resource(PointerState)
# current_targets = self.world.query_entities(HoverIntention)

# difference between both

from omniecs.world import WorldFactory
from ui.components.behavior import Enabled, HoverIntention, Hovered
from ui.resources.state import PointerState
from ui.systems.behaviour_system import HoverSystem


def test_no_hover_intention_or_hovered():
    world = WorldFactory.create_world()
    world.register_system(HoverSystem())
    world.set_resource(PointerState())

    world.spawn(Enabled())
    world.execute(0)

    pointer = world.get_resource(PointerState)
    assert pointer.hovered_entities == set()
    assert world.query_entities(all_of=(Hovered,)) == set()

def test_adding_hover_intentions():
    world = WorldFactory.create_world()
    world.register_system(HoverSystem())
    world.set_resource(PointerState())

    entity_id1 = world.spawn(HoverIntention())
    entity_id2 = world.spawn(HoverIntention())
    world.execute(0)

    pointer = world.get_resource(PointerState)
    assert pointer.hovered_entities == set([entity_id1, entity_id2])
    assert world.query_entities(all_of=(Hovered,)) == set([entity_id1, entity_id2])

def test_removing_hovered():
    world = WorldFactory.create_world()
    world.register_system(HoverSystem())

    entity_id1 = world.spawn(Enabled())
    entity_id2 = world.spawn(Enabled())
    world.set_resource(PointerState(hovered_entities=set([entity_id1, entity_id2])))
    world.execute(0)

    pointer = world.get_resource(PointerState)
    assert pointer.hovered_entities == set([])
    assert world.query_entities(all_of=(Hovered,)) == set([])

def test_changing_hovered():
    world = WorldFactory.create_world()
    world.register_system(HoverSystem())

    entity_id1 = world.spawn(Enabled())
    world.spawn(Enabled())
    entity_id3 = world.spawn(HoverIntention())
    world.set_resource(PointerState(hovered_entities=set([entity_id1])))
    world.execute(0)

    pointer = world.get_resource(PointerState)
    assert pointer.hovered_entities == set([entity_id3])
    assert world.query_entities(all_of=(Hovered,)) == set([entity_id3])