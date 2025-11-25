from pathlib import Path
from pydantic import BaseModel


class AssetServiceConfig(BaseModel):
    data_loader: str
    search_path: Path
