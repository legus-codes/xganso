from pathlib import Path
from typing import List, Protocol


class FileSystemProtocol(Protocol):
    
    @staticmethod
    def glob(base_path: Path, pattern: str) -> List[Path]:
        ...


class LocalFileSystem:

    @staticmethod
    def glob(base_path: Path, pattern: str) -> List[Path]:
        return list(base_path.rglob(pattern))
