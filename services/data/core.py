from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Protocol

from services.data.data_models import DataDescription


class DataType(Enum):
    UNIT = auto()
    

@dataclass
class DataManagerError:
    filename: str
    message: str


class DataManagerProtocol(Protocol):
    
    def load(self) -> List[DataManagerError]:
        ...

    def reload(self) -> List[DataManagerError]:
        ...

    def get(self, identifier: str) -> DataDescription | None:
        ...

