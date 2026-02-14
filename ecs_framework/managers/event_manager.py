from ecs_framework.primitives import Event
from ecs_framework.protocols import EventManagerProtocol


class EventManager(EventManagerProtocol):

    def __init__(self):
        self._events: list[Event] = []

    def push(self, event: Event) -> None:
        self._events.append(event)

    def get(self) -> list[Event]:
        return self._events

    def clear(self) -> None:
        self._events.clear()
