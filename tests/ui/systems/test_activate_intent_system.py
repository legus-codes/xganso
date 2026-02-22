from adapters.input.events import MouseButton
from ecs_framework.system import ClearTemporaryComponentSystem
from ecs_framework.types import ExecutionStage
from ecs_framework.world import WorldFactory
from ui.components.behavior import ActivateIntent, Hovered, Pressed
from ui.resources.state import PointerState
from ui.systems.intent_system import ActivateIntentSystem


def test_no_activate_intent():
    world = WorldFactory.create_world()
    world.register_system(ActivateIntentSystem(), ExecutionStage.update)
    world.unregister_system(ClearTemporaryComponentSystem)
    world.set_resource(PointerState())

    world.spawn(Hovered(), Pressed())
    world.execute(0)

    assert world.query_entities(all_of=(ActivateIntent,)) == set()

def test_hovered_and_pressed_activate_intent():
    world = WorldFactory.create_world()
    world.register_system(ActivateIntentSystem(), ExecutionStage.update)
    world.unregister_system(ClearTemporaryComponentSystem)
    world.set_resource(PointerState(buttons_released=set([MouseButton.left])))

    entity_id = world.spawn(Hovered(), Pressed())
    world.execute(0)

    assert entity_id in world.query_entities(all_of=(ActivateIntent,))

def test_activate_intent_is_cleared_correctly():
    world = WorldFactory.create_world()
    world.register_system(ActivateIntentSystem(), ExecutionStage.update)
    world.set_resource(PointerState(buttons_released=set([MouseButton.left])))

    world.spawn(Hovered(), Pressed())
    world.execute(0)

    assert world.query_entities(all_of=(ActivateIntent,)) == set()

def test_hovered_not_pressed_activated_intent():
    world = WorldFactory.create_world()
    world.register_system(ActivateIntentSystem(), ExecutionStage.update)
    world.unregister_system(ClearTemporaryComponentSystem)
    world.set_resource(PointerState(buttons_released=set([MouseButton.left])))

    world.spawn(Hovered())
    world.execute(0)

    assert world.query_entities(all_of=(ActivateIntent,)) == set()

def test_not_hovered_pressed_activated_intent():
    world = WorldFactory.create_world()
    world.register_system(ActivateIntentSystem(), ExecutionStage.update)
    world.unregister_system(ClearTemporaryComponentSystem)
    world.set_resource(PointerState(buttons_released=set([MouseButton.left])))

    world.spawn(Pressed())
    world.execute(0)

    assert world.query_entities(all_of=(ActivateIntent,)) == set()
