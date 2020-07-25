import os
import shutil
from pathlib import Path
from typing import Iterator

from Model.CopyResult import CopyResult
from DestinationPathCreator.AbstractDestinationPathCreator import AbstractDestinationPathCreator


class PhotoCopier(object):

    ORIGINAL_PHOTOS_DIRECTORY = 'Masters'

    __destinationPath = None
    __sourcePath = None
    __destinationPathCreator = None

    def __init__(self, rawSourcePath: str, rawDestinationPath: str, writeMode: AbstractDestinationPathCreator):
        self.__destinationPath = Path(rawDestinationPath)
        self.__sourcePath = Path(rawSourcePath)
        self.__destinationPathCreator = writeMode

        self.validateSource()
        self.validateDestination()

    def copyAll(self, dryRun: bool = False) -> Iterator[CopyResult]:
        numberOfSourcePhotos = self.countSourcePhotos()
        numberOfCopiedPhotos = 0

        yield CopyResult(numberOfSourcePhotos, numberOfCopiedPhotos)

        for yearDirectory in self.getYearDirectories():
            year = yearDirectory.name
            for monthDirectory in self.getMonthDirectories(yearDirectory):
                month = monthDirectory.name
                for dayDirectory in self.getDayDirectories(monthDirectory):
                    day = dayDirectory.name
                    for photo in self.getAllPhotosFromDay(dayDirectory):
                        newPhotoPath = self.__destinationPathCreator.createPath(year, month, day, photo, self.__destinationPath)
                        self.copyPhoto(photo, newPhotoPath, dryRun)
                        numberOfCopiedPhotos += 1

                        yield CopyResult(numberOfSourcePhotos, numberOfCopiedPhotos)

    def countSourcePhotos(self) -> int:
        numberOfSourcePhotos = 0
        for yearDirectory in self.getYearDirectories():
            for monthDirectory in self.getMonthDirectories(yearDirectory):
                for dayDirectory in self.getDayDirectories(monthDirectory):
                    for photo in self.getAllPhotosFromDay(dayDirectory):
                        numberOfSourcePhotos += 1

        return numberOfSourcePhotos

    def copyPhoto(self, photo: Path, newPhotoPath: Path, dryRun: bool):
        newPhotoPath.parent.mkdir(parents=True, exist_ok=True)
        newPhotoPath.touch()
        if not dryRun:
            shutil.copy2(str(photo), str(newPhotoPath))

    def getAllPhotosFromDay(self, dayDirectory: Path) -> Iterator[Path]:
        for daySubDirectory in dayDirectory.glob('*'):
            if dayDirectory.is_dir():
                for photo in daySubDirectory.glob('*.JPG'):
                    yield photo

    def getDayDirectories(self, monthDirectory: Path) -> Iterator[Path]:
        for dayDirectory in monthDirectory.glob('*'):
            if dayDirectory.is_dir():
                yield dayDirectory

    def getMonthDirectories(self, yearDirectory: Path) -> Iterator[Path]:
        for monthDirectory in yearDirectory.glob('*'):
            if monthDirectory.is_dir():
                yield monthDirectory

    def getYearDirectories(self) -> Iterator[Path]:
        for yearDirectory in self.__sourcePath.glob(self.ORIGINAL_PHOTOS_DIRECTORY + '/*'):
            if yearDirectory.is_dir():
                yield yearDirectory

    def validateDirectory(self, directory: Path):
        if not directory.exists():
            raise IOError('Directory "'+str(directory)+'" does not exist.')

        if not directory.is_dir():
            raise IOError('Directory "' + str(directory) + '" is not a directory.')

    def validateDestination(self):
        self.validateDirectory(self.__destinationPath)

        if len(os.listdir(self.__destinationPath)) > 0:
            raise IOError('Destination directory is not empty')

    def validateSource(self):
        self.validateDirectory(self.__sourcePath)

        if not self.__sourcePath.name.endswith('.photoslibrary'):
            raise IOError('Source directory is not an iCloud Photos library')
