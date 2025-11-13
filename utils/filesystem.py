from pathlib import Path
from typing import List, Protocol


class FilesystemProviderProtocol(Protocol):
    
    @staticmethod
    def glob(base_path: Path, pattern: str) -> List[Path]:
        ...


class LocalFilesystemProvider:

    @staticmethod
    def glob(base_path: Path, pattern: str) -> List[Path]:
        return list(base_path.rglob(pattern))
