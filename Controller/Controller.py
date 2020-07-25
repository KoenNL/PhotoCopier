import argparse

from Service.PhotoCopier import PhotoCopier
from DestinationPathCreator.DateFilename import DateFilename
from DestinationPathCreator.YearMonthDirectories import YearMonthDirectories


class Controller(object):
    fileStructures = {}
    parser = None

    def __init__(self):
        self.fileStructures = {
            'dateFilename': DateFilename(),
            'yearMonthDirectories': YearMonthDirectories()
        }

        self.parser = argparse.ArgumentParser('Photo Copier')
        self.parser.add_argument(
            'source',
            help='An absolute path to an iCloud Photos library',
            type=str
        )
        self.parser.add_argument(
            'destination',
            help='An absolute path to an empty directory to copy the new photos to',
            type=str
        )
        self.parser.add_argument(
            '--file-structure',
            help='Select a file structure for the destination. Choose: ' + ' or '.join(self.fileStructures.keys())
                 + '. Default: yearMonthDirectories.',
            type=str,
            required=False,
            default='yearMonthDirectories'
        )
        self.parser.add_argument(
            '--dry-run',
            help='Do a dry run. All destination files will be created, but they will all be empty.',
            required=False,
            type=bool,
            default=False
        )

    def askConfirmation(self, source: str, destination: str, dryRun: bool):
        if dryRun:
            print(
                'Are you sure you want to do a dry run to copy all the photos from "' + source + '" to "'
                + destination + '"? [y/n]: ', end='')
        else:
            print(
                'Are you sure you want to copy all the photos from "' + source + '" to "'
                + destination + '"? [y/n]: ', end='')
        response = input()

        if response == 'y':
            return True
        if response == 'n':
            return False

        return None

    def run(self):
        arguments = self.parser.parse_args()

        source = arguments.source
        destination = arguments.destination
        dryRun = arguments.dry_run
        fileStructure = arguments.file_structure

        if fileStructure not in self.fileStructures:
            print('Invalid file structure "' + fileStructure + '" selected. Choose either ' + ' or '.join(
                self.fileStructures.keys()))
            exit(1)

        confirmation = self.askConfirmation(source, destination, dryRun)
        while confirmation is None:
            confirmation = self.askConfirmation(source, destination, dryRun)

        if not confirmation:
            print('Process terminated by user')
            exit(1)

        print('Starting photo copier...')
        photoCopier = None
        try:
            photoCopier = PhotoCopier(source, destination, self.fileStructures[fileStructure])
        except IOError as exception:
            print(exception)
            exit(1)

        for copyResult in photoCopier.copyAll(dryRun):
            print(str(copyResult.numberOfCopiedPhotos) + ' of ' + str(
                copyResult.numberOfSourcePhotos) + ' photos copied. '
                  + str(copyResult.percentageDone) + '% complete.', end='\r')

        print('\nDone!')
