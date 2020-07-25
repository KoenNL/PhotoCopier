class CopyResult(object):

    numberOfSourcePhotos = 0
    numberOfCopiedPhotos = 0
    percentageDone = 0

    def __init__(self, numberOfSourcePhotos: int, numberOfCopiedPhotos: int):
        self.numberOfSourcePhotos = numberOfSourcePhotos
        self.numberOfCopiedPhotos = numberOfCopiedPhotos

        if numberOfSourcePhotos > 0 and numberOfCopiedPhotos > 0:
            self.percentageDone = int((numberOfCopiedPhotos / numberOfSourcePhotos) * 100)

    def getNumberOfSourcePhotos(self) -> int:
        return self.numberOfSourcePhotos

    def getNumberOfCopiedPhotos(self) -> int:
        return self.numberOfCopiedPhotos

    def getPercentageDone(self) -> int:
        return self.percentageDone
