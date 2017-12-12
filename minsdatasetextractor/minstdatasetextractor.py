#!/usr/bin/env python3
# imports
from enum import Enum, unique
from os import stat
# contantes
FILE_MODE="rb"
ENDIAN="big"
# data type size
@unique
class DataTypeSize(Enum):
    INTEGER_SIZE=4
    BYTE_SIZE=1
    pass
pass
# header size
@unique
class HeaderSize(Enum):
    LABEL=2
    IMAGE=4
    pass
pass
# header size
@unique
class MagicNumber(Enum):
    LABEL=2049
    IMAGE=2051
    pass
pass
# pattern types
@unique
class Pattern(Enum):
    TRAINING="training"
    TEST="test"
    pass
pass
# MINST data set extractor
class MinstDataSetExtractor():
    # extract data set
    def extractDataSet(self):
        labels=self.extractLabels()
        pass
    # extract labels
    def extractLabels(self):
        # get file size
        fileSize=stat(self.labelsFileName).st_size
        # read file
        with open(self.labelsFileName, FILE_MODE) as labelsFile:
            # read header
            for index in range(0,HeaderSize.LABEL.value):
                bytes = labelsFile.read(DataTypeSize.INTEGER_SIZE.value)
                if index==0 :
                    magicNumber=int.from_bytes(bytes, byteorder=ENDIAN)
                else:
                    labelsNumber = int.from_bytes(bytes, byteorder=ENDIAN)
                    self.checkLabelsFile(fileSize, magicNumber, labelsNumber)
            # read body
            byte = None
            while byte != b"":
                # Do stuff with byte.
                byte = labelsFile.read(DataTypeSize.BYTE_SIZE.value)
                pass
            pass
        pass
    # check labels file
    def checkLabelsFile(self,fileSize,magicNumber,labelsNumber):
        # check magic number
        if MagicNumber.LABEL.value != magicNumber:
            raise Exception('Labels magic number does not match : expected=' + str(MagicNumber.LABEL.value) + " actual="+str(magicNumber))
        # check size
        expectedSize=labelsNumber+(HeaderSize.LABEL.value*DataTypeSize.INTEGER_SIZE.value)
        if expectedSize != fileSize:
            raise Exception('Labels file size does not match : expected=' + str(expectedSize) + " actual="+str(fileSize))
    # constructor
    def __init__(self, labelsFileName, imagesFileName,patternValue):
        self.labelsFileName=labelsFileName
        self.imagesFileName=imagesFileName
        self.patternValue=patternValue
        pass
    pass
# run extractor
if __name__ == '__main__':
    labelsFileName="/mnt/hgfs/shared/Documents/myDevelopment/MNISTdataSetExtractor/ExtractedDataSet/t10k-labels.idx1-ubyte"
    imagesFileName = "/mnt/hgfs/shared/Documents/myDevelopment/MNISTdataSetExtractor/ExtractedDataSet/t10k-images-idx3-ubyte"
    patternValue=Pattern.TEST.value
    mdse=MinstDataSetExtractor(labelsFileName, imagesFileName,patternValue)
    mdse.extractDataSet()
    pass
pass
