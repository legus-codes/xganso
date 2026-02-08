from typing import List


class Event: ...


class EventManager:

    def __init__(self):
        self._events: List[Event] = []

    def push(self, event: Event) -> None:
        self._events.append(event)

    def drain(self) -> List[Event]:
        events = self._events
        self._events = []
        return events

    def clear(self) -> None:
        self._events.clear()
