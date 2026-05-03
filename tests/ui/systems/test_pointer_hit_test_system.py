from core.primitives import IVec2
from omniecs.world import World, WorldFactory
from ui.components.behavior import Enabled, HoverIntent, Hoverable
from ui.components.layout import RenderLayer, WorldTransform
from ui.resources.state import PointerState
from ui.systems.intent_system import PointerHitTestSystem


def create_world() -> World:
    world = WorldFactory.create_empty_world()
    world.register_system(PointerHitTestSystem())
    world.set_resource(PointerState(position=IVec2(10, 10)))
    return world

def test_pointer_hit_test():
    world = create_world()

    entity_id = world.spawn(WorldTransform(IVec2(5, 5), IVec2(10, 10)), RenderLayer(0), Enabled(), Hoverable())
    world.execute()

    assert entity_id in world.query_entities(all_of=(HoverIntent,))

def test_pointer_hit_miss_test():
    world = create_world()

    entity_id = world.spawn(WorldTransform(IVec2(15, 15), IVec2(10, 10)), RenderLayer(0), Enabled(), Hoverable())
    world.execute()

    assert entity_id not in world.query_entities(all_of=(HoverIntent,))

def test_pointer_hit_with_multiple_entities_test():
    world = create_world()

    world.spawn(WorldTransform(IVec2(5, 5), IVec2(10, 10)), RenderLayer(0), Enabled(), Hoverable())
    entity_id = world.spawn(WorldTransform(IVec2(5, 5), IVec2(10, 10)), RenderLayer(2), Enabled(), Hoverable())
    world.spawn(WorldTransform(IVec2(5, 5), IVec2(10, 10)), RenderLayer(1), Enabled(), Hoverable())
    world.execute()

    assert entity_id in world.query_entities(all_of=(HoverIntent,))
