from abc import ABC, abstractmethod
from pathlib import Path


class AbstractDestinationPathCreator(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def createPath(self, year: str, month: str, day: str, photoPath: Path, destinationPath: Path) -> Path:
        pass
