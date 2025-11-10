from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, Protocol

from pydantic import BaseModel

from services.data.models import DataDescription


class DataType(Enum):
    UNIT = 'Unit'
    

@dataclass
class DataManagerError:
    filename: str
    message: str


class DataManagerConfig(BaseModel):
    type: DataType
    model: str
    repository: str
    data_path: Path


class DataServiceConfig(BaseModel):
    data_managers: List[DataManagerConfig]


class DataManagerProtocol(Protocol):

    def load(self) -> List[DataManagerError]:
        ...

    def reload(self) -> List[DataManagerError]:
        ...

    def get(self, identifier: str) -> DataDescription | None:
        ...
