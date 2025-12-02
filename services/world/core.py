from typing import Dict, List
from pydantic import BaseModel


class WorldServiceConfig(BaseModel):
    components: Dict[str, List[str]]
