from enum import Enum, auto
from typing import Dict, Protocol

from services.data.data_models import DataDescription


class DataType(Enum):
    UNIT = auto()
    

class DataManagerProtocol(Protocol):
    
    def load(self) -> Dict[str, str]:
        ...

    def reload(self) -> Dict[str, str]:
        ...

    def get(self, identifier: str) -> DataDescription | None:
        ...

