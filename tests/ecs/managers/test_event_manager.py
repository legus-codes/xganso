from ecs_framework.managers.event_manager import Event, EventManager


def test_create_event():
    event_manager = EventManager()
    event_manager.push(Event())
    assert len(event_manager._events) == 1

    
def test_drain_events():
    event_manager = EventManager()
    event_manager.push(Event())
    event_manager.push(Event())
    event_manager.push(Event())
    events = event_manager.drain()
    assert len(events) == 3
    assert len(event_manager._events) == 0

    
def test_clear_events():
    event_manager = EventManager()
    event_manager.push(Event())
    event_manager.push(Event())
    event_manager.push(Event())
    event_manager.clear()
    assert len(event_manager._events) == 0
