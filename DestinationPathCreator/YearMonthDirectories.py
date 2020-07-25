from pathlib import Path

from DestinationPathCreator.AbstractDestinationPathCreator import AbstractDestinationPathCreator


class YearMonthDirectories(AbstractDestinationPathCreator):

    def createPath(self, year: str, month: str, day: str, photoPath: Path, destinationPath: Path):
        return Path(destinationPath/year/month/photoPath.name.replace('._', ''))
