from dataclasses import dataclass

from omniecs.types import Event, EntityId


@dataclass(slots=True)
class DeselectItemEvent(Event):
    radio_group: str
    selected_item: EntityId
