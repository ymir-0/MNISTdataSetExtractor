#!/usr/bin/env python3
# imports
from enum import Enum, unique
from os import stat
# contantes
FILE_MODE="rb"
ENDIAN="big"
END_OF_FILE=b""
# data type size
@unique
class DataTypeSize(Enum):
    INTEGER_SIZE=4
    BYTE_SIZE=1
# header size
@unique
class HeaderSize(Enum):
    LABEL=2
    IMAGE=4
# header size
@unique
class MagicNumber(Enum):
    LABEL=2049
    IMAGE=2051
# pattern types
@unique
class Pattern(Enum):
    TRAINING="training"
    TEST="test"
# MINST data set extractor
class MinstDataSetExtractor():
    # extract data set
    def extractDataSet(self):
        # extract separated data
        labels=self.extractLabels()
        images = self.extractImages()
        # check size consistancy labels / images
        if len(labels)!=len(images):
            raise Exception('Size between labels & images does not match : labels=' + str(len(labels)) + " images=" + str(len(images)))
        #
        pass
    # extract labels
    def extractLabels(self):
        # get file size
        fileSize=stat(self.labelsFileName).st_size
        # read file
        with open(self.labelsFileName, FILE_MODE) as labelsFile:
            # read header
            for index in range(0,HeaderSize.LABEL.value):
                binaryValue = labelsFile.read(DataTypeSize.INTEGER_SIZE.value)
                numericValue=int.from_bytes(binaryValue, byteorder=ENDIAN)
                if index==0 :
                    magicNumber=numericValue
                else:
                    labelsNumber = numericValue
                    self.checkLabelsFile(fileSize, magicNumber, labelsNumber)
            # read body
            labels=dict()
            index=0
            while binaryValue != END_OF_FILE:
                binaryValue = labelsFile.read(DataTypeSize.BYTE_SIZE.value)
                numericValue=int.from_bytes(binaryValue, byteorder=ENDIAN)
                labels[index]=str(numericValue)
                index=index+1
            labelsFile.close()
        return labels
    # check labels file
    def checkLabelsFile(self,fileSize,magicNumber,labelsNumber):
        # check magic number
        if MagicNumber.LABEL.value != magicNumber:
            raise Exception('Labels magic number does not match : expected=' + str(MagicNumber.LABEL.value) + " actual="+str(magicNumber))
        # check size
        expectedSize=labelsNumber+(HeaderSize.LABEL.value*DataTypeSize.INTEGER_SIZE.value)
        if expectedSize != fileSize:
            raise Exception('Labels file size does not match : expected=' + str(expectedSize) + " actual="+str(fileSize))
    # extract images
    def extractImages(self):
        # get file size
        fileSize=stat(self.imagesFileName).st_size
        # read file
        with open(self.imagesFileName, FILE_MODE) as imagesFile:
            # read header
            for index in range(0,HeaderSize.IMAGE.value):
                binaryValue = imagesFile.read(DataTypeSize.INTEGER_SIZE.value)
                numericValue=int.from_bytes(binaryValue, byteorder=ENDIAN)
                if index==0 :
                    magicNumber=numericValue
                elif index == 1:
                    imagesNumber = numericValue
                elif index == 2:
                    rowsNumber = numericValue
                else:
                    columnsNumber = numericValue
                    pixelNumbers = rowsNumber * columnsNumber
                    self.checkImagesFile(fileSize, magicNumber, imagesNumber,pixelNumbers)
            # read body
            images=dict()
            pixels=list()
            imageIndex=0
            pixelIndex=0
            while binaryValue != END_OF_FILE:
                # read image
                if pixelIndex<pixelNumbers:
                    binaryValue = imagesFile.read(DataTypeSize.BYTE_SIZE.value)
                    numericValue=int.from_bytes(binaryValue, byteorder=ENDIAN)
                    pixels.append(numericValue)
                    pixelIndex=pixelIndex+1
                # add image to dictionary
                else:
                    images[imageIndex]=pixels
                    imageIndex=imageIndex+1
                    pixels = list()
                    pixelIndex = 0
            imagesFile.close()
        return images
    # check images file
    def checkImagesFile(self,fileSize,magicNumber,imagesNumber,pixelNumbers):
        # check magic number
        if MagicNumber.IMAGE.value != magicNumber:
            raise Exception('Images magic number does not match : expected=' + str(MagicNumber.IMAGE.value) + " actual="+str(magicNumber))
        # check size
        expectedSize=(imagesNumber*pixelNumbers)+(HeaderSize.IMAGE.value*DataTypeSize.INTEGER_SIZE.value)
        if expectedSize != fileSize:
            raise Exception('Images file size does not match : expected=' + str(expectedSize) + " actual="+str(fileSize))
    # constructor
    def __init__(self, labelsFileName, imagesFileName,patternValue):
        self.labelsFileName=labelsFileName
        self.imagesFileName=imagesFileName
        self.patternValue=patternValue
# run extractor
if __name__ == '__main__':
    labelsFileName="/mnt/hgfs/shared/Documents/myDevelopment/MNISTdataSetExtractor/ExtractedDataSet/t10k-labels.idx1-ubyte"
    imagesFileName = "/mnt/hgfs/shared/Documents/myDevelopment/MNISTdataSetExtractor/ExtractedDataSet/t10k-images.idx3-ubyte"
    patternValue=Pattern.TEST.value
    mdse=MinstDataSetExtractor(labelsFileName, imagesFileName,patternValue)
    mdse.extractDataSet()
    pass
pass
