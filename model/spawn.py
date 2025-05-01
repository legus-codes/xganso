from dataclasses import dataclass
from enum import IntEnum
from typing import List, Optional


class SpawnType(IntEnum):
    NONE = 0
    TEAM_RED = 1
    TEAM_BLUE = 2
    TEAM_GREEN = 3
    TEAM_YELLOW = 4


@dataclass(frozen=True)
class Spawn:
    spawn_type: SpawnType
    color: str
    text_color: str

    @property
    def name(self) -> str:
        return self.spawn_type.name.replace('_', ' ').title()

    @property
    def value(self) -> int:
        return self.spawn_type.value


class SpawnLibrary:

    spawns = {
        SpawnType.NONE: Spawn(SpawnType.NONE, 'black', 'beige'),
        SpawnType.TEAM_RED: Spawn(SpawnType.TEAM_RED, 'red', 'black'),
        SpawnType.TEAM_BLUE: Spawn(SpawnType.TEAM_BLUE, 'blue', 'black'),
        SpawnType.TEAM_GREEN: Spawn(SpawnType.TEAM_GREEN, 'green', 'black'),
        SpawnType.TEAM_YELLOW: Spawn(SpawnType.TEAM_YELLOW, 'yellow', 'black'),
    }

    @classmethod
    def count(cls) -> int:
        return len(cls.spawns)

    @classmethod
    def get(cls, spawn_type: str|SpawnType) -> Optional[Spawn]:
        if isinstance(spawn_type, str):
            spawn_type = SpawnType[spawn_type]
        return cls.spawns.get(spawn_type, None)
    
    @classmethod
    def none(cls) -> Spawn:
        return cls.spawns[SpawnType.NONE]

    @classmethod
    def default(cls) -> Spawn:
        return cls.spawns[SpawnType.TEAM_RED]

    @classmethod
    def values(cls) -> List[Spawn]:
        return [spawn for spawn in cls.spawns.values() if spawn != cls.none()]
