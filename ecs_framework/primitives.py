from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Protocol


@dataclass(slots=True, frozen=True)
class EntityId:
    value: int


class ComponentProtocol: ...


class Bundle(Protocol):
    def components(self) -> Iterable[ComponentProtocol]: ...


class SystemProtocol(Protocol):
    def execute(self, delta_time: float) -> None: ...


class Resource: ...


class Event: ...


class DrawCommand(Protocol):
    def layer(self) -> int: ...


class ExecutionStage(Enum):
    reset = 0
    update = 1
    cleanup = 2
