from enum import Enum
from pathlib import Path
from typing import List, Protocol

from pydantic import BaseModel

from services.core import LoadingError
from services.data.models import DataDescription


class DataType(Enum):
    UNIT = 'Unit'


class DataManagerConfig(BaseModel):
    type: DataType
    data_model: str
    data_loader: str
    search_path: Path


class DataServiceConfig(BaseModel):
    data_managers: List[DataManagerConfig]


class DataManagerProtocol(Protocol):

    def load(self) -> List[LoadingError]:
        ...

    def reload(self) -> List[LoadingError]:
        ...

    def get(self, identifier: str) -> DataDescription | None:
        ...
