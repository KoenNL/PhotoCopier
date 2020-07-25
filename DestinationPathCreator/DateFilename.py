from pathlib import Path

from DestinationPathCreator.AbstractDestinationPathCreator import AbstractDestinationPathCreator


class DateFilename(AbstractDestinationPathCreator):
    def createPath(self, year: str, month: str, day: str, photoPath: Path, destinationPath: Path):
        newPhotoFilename = year+'-'+month+'-'+day+'.'+photoPath.suffix
        return Path(destinationPath/newPhotoFilename)
