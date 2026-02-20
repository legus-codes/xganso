from core.primitives import IVec2
from ecs_framework.types import ExecutionStage
from ecs_framework.world import WorldFactory
from ui.components.behavior import Enabled, Hoverable, Hovered
from ui.components.layout import RenderLayer, WorldTransform
from ui.resources.state import PointerState
from ui.systems.hit_test_system import PointerHitTestSystem


def test_pointer_hit_test():
    world = WorldFactory.create_world()
    world.register_system(PointerHitTestSystem(), ExecutionStage.update)
    world.set_resource(PointerState(position=IVec2(10, 10)))

    entity_id = world.spawn(WorldTransform(IVec2(5, 5), IVec2(10, 10)), RenderLayer(0), Enabled(), Hoverable())
    world.execute(0)

    pointer = world.get_resource(PointerState)
    assert entity_id in world.query_entities(all_of=(Hovered,))
    assert pointer.hovered_entity == entity_id

def test_pointer_hit_miss_test():
    world = WorldFactory.create_world()
    world.register_system(PointerHitTestSystem(), ExecutionStage.update)
    world.set_resource(PointerState(position=IVec2(10, 10)))

    entity_id = world.spawn(WorldTransform(IVec2(15, 15), IVec2(10, 10)), RenderLayer(0), Enabled(), Hoverable())
    world.execute(0)

    pointer = world.get_resource(PointerState)
    assert entity_id not in world.query_entities(all_of=(Hovered,))
    assert pointer.hovered_entity is None

def test_pointer_hit_with_multiple_entities_test():
    world = WorldFactory.create_world()
    world.register_system(PointerHitTestSystem(), ExecutionStage.update)
    world.set_resource(PointerState(position=IVec2(10, 10)))

    world.spawn(WorldTransform(IVec2(5, 5), IVec2(10, 10)), RenderLayer(0), Enabled(), Hoverable())
    entity_id = world.spawn(WorldTransform(IVec2(5, 5), IVec2(10, 10)), RenderLayer(2), Enabled(), Hoverable())
    world.spawn(WorldTransform(IVec2(5, 5), IVec2(10, 10)), RenderLayer(1), Enabled(), Hoverable())
    world.execute(0)

    pointer = world.get_resource(PointerState)
    assert entity_id in world.query_entities(all_of=(Hovered,))
    assert pointer.hovered_entity == entity_id

def test_new_entity_hit_test():
    world = WorldFactory.create_world()
    world.register_system(PointerHitTestSystem(), ExecutionStage.update)
    world.set_resource(PointerState(position=IVec2(10, 10)))

    entity_id1 = world.spawn(WorldTransform(IVec2(5, 5), IVec2(10, 10)), RenderLayer(0), Enabled(), Hoverable())
    world.execute(0)

    pointer = world.get_resource(PointerState)
    assert entity_id1 in world.query_entities(all_of=(Hovered,))
    assert pointer.hovered_entity == entity_id1

    entity_id2 = world.spawn(WorldTransform(IVec2(5, 5), IVec2(10, 10)), RenderLayer(1), Enabled(), Hoverable())
    world.execute(0)

    pointer = world.get_resource(PointerState)
    assert entity_id1 not in world.query_entities(all_of=(Hovered,))
    assert entity_id2 in world.query_entities(all_of=(Hovered,))
    assert pointer.hovered_entity == entity_id2

def test_no_entity_hit_test():
    world = WorldFactory.create_world()
    world.register_system(PointerHitTestSystem(), ExecutionStage.update)
    world.set_resource(PointerState(position=IVec2(10, 10)))

    entity_id = world.spawn(WorldTransform(IVec2(5, 5), IVec2(10, 10)), RenderLayer(0), Enabled(), Hoverable())
    world.execute(0)

    pointer = world.get_resource(PointerState)
    assert entity_id in world.query_entities(all_of=(Hovered,))
    assert pointer.hovered_entity == entity_id

    world.remove_component(entity_id, Enabled)
    world.execute(0)

    pointer = world.get_resource(PointerState)
    assert entity_id not in world.query_entities(all_of=(Hovered,))
    assert pointer.hovered_entity is None
