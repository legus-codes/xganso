from core.primitives import IVec2
from ecs_framework.system import ClearTemporaryComponentSystem
from ecs_framework.types import ExecutionStage
from ecs_framework.world import WorldFactory
from ui.components.behavior import Enabled, HoverIntention, Hoverable
from ui.components.layout import RenderLayer, WorldTransform
from ui.resources.state import PointerState
from ui.systems.hit_test_system import PointerHitTestSystem


def test_pointer_hit_test():
    world = WorldFactory.create_world()
    world.register_system(PointerHitTestSystem(), ExecutionStage.update)
    world.unregister_system(ClearTemporaryComponentSystem)
    world.set_resource(PointerState(position=IVec2(10, 10)))

    entity_id = world.spawn(WorldTransform(IVec2(5, 5), IVec2(10, 10)), RenderLayer(0), Enabled(), Hoverable())
    world.execute(0)

    assert entity_id in world.query_entities(all_of=(HoverIntention,))

def test_pointer_hit_miss_test():
    world = WorldFactory.create_world()
    world.register_system(PointerHitTestSystem(), ExecutionStage.update)
    world.unregister_system(ClearTemporaryComponentSystem)
    world.set_resource(PointerState(position=IVec2(10, 10)))

    entity_id = world.spawn(WorldTransform(IVec2(15, 15), IVec2(10, 10)), RenderLayer(0), Enabled(), Hoverable())
    world.execute(0)

    assert entity_id not in world.query_entities(all_of=(HoverIntention,))

def test_pointer_hit_with_multiple_entities_test():
    world = WorldFactory.create_world()
    world.register_system(PointerHitTestSystem(), ExecutionStage.update)
    world.unregister_system(ClearTemporaryComponentSystem)
    world.set_resource(PointerState(position=IVec2(10, 10)))

    world.spawn(WorldTransform(IVec2(5, 5), IVec2(10, 10)), RenderLayer(0), Enabled(), Hoverable())
    entity_id = world.spawn(WorldTransform(IVec2(5, 5), IVec2(10, 10)), RenderLayer(2), Enabled(), Hoverable())
    world.spawn(WorldTransform(IVec2(5, 5), IVec2(10, 10)), RenderLayer(1), Enabled(), Hoverable())
    world.execute(0)

    assert entity_id in world.query_entities(all_of=(HoverIntention,))
