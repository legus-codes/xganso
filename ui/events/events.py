from dataclasses import dataclass

from omniecs.types import Event, EntityId


@dataclass(slots=True)
class DeselectGroupEvent(Event):
    group: str
    selected: EntityId


@dataclass(slots=True)
class LoseFocusEvent(Event):
    focused: EntityId
