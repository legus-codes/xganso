from ecs_framework.managers import EventManager
from ecs_framework.types import Event


def test_create_event():
    event_manager = EventManager()
    event_manager.push(Event())
    assert len(event_manager._events) == 1

    
def test_get_events():
    event_manager = EventManager()
    event_manager.push(Event())
    event_manager.push(Event())
    event_manager.push(Event())
    events = event_manager.get()
    assert len(events) == 3
    assert len(event_manager._events) == 3

    
def test_clear_events():
    event_manager = EventManager()
    event_manager.push(Event())
    event_manager.push(Event())
    event_manager.push(Event())
    event_manager.clear()
    assert len(event_manager._events) == 0
