from ecs_framework.primitives import Event


class EventManager:

    def __init__(self):
        self._events: list[Event] = []

    def push(self, event: Event) -> None:
        self._events.append(event)

    def drain(self) -> list[Event]:
        events = self._events
        self._events = []
        return events

    def clear(self) -> None:
        self._events.clear()
