#!/usr/bin/env python3
# imports
from inspect import signature
from enum import Enum, unique
from os import stat,makedirs,linesep
from os.path import join, exists, isdir
from json import dumps, loads
from pythoncommontools.logger import logger
from pythoncommontools.objectUtil.objectUtil import methodArgsStringRepresentation
from pythoncommontools.configurationLoader import configurationLoader
# contantes
CONFIGURATION_FILE=join("..","conf","minsdatasetextractor.conf")
ENDIAN="big"
IMAGE_MARKUP="image"
TEST_FILE_EXTENSION=".json"
REPRENSATION_INTERVAL=51.2 # we have 256 grey level and 5 gradient char. 256/5=51.2
REPRENSATION_GRADIENT=(" ","░","▒","▓","█")
# load configuration
configurationLoader.loadConfiguration( CONFIGURATION_FILE )
logger.loadLogger("MinstDataSetExtractor",CONFIGURATION_FILE)
# file mode
@unique
class FileMode(Enum):
    BINARY="rb"
    TEST_WRITE="wt"
    TEST_READ="rt"
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
    TRAINING="TRAINING"
    TEST="TEST"
    @staticmethod
    def listValues():
        values=list()
        for pattern in Pattern: values.append(pattern.value.upper())
        return values
# test datum
class TestData():
    # constructor
    def __init__(self, width=0, height=0, image=[], label="",pattern=""):
        # logger context
        argsStr = methodArgsStringRepresentation(signature(TestData.__init__).parameters,locals())
        # logger input
        logger.loadedLogger.input(__name__, TestData.__name__, TestData.__init__.__name__,message=argsStr)
        # construct object
        self.width = width
        self.height = height
        self.image = image
        self.label = label
        self.pattern = pattern
        # logger output
        logger.loadedLogger.output(__name__, TestData.__name__, TestData.__init__.__name__)
    def load(self, fileName):
        # logger context
        argsStr = methodArgsStringRepresentation(signature(TestData.__init__).parameters, locals())
        # logger input
        logger.loadedLogger.input(__name__, TestData.__name__, TestData.__init__.__name__, message=argsStr)
        # construct object
        file = open(fileName, FileMode.TEST_READ.value)
        jsonTestData=file.read()
        file.close()
        loadedDict = loads(jsonTestData)
        self.__dict__.update(loadedDict)
        # logger output
        logger.loadedLogger.output(__name__, TestData.__name__, TestData.__init__.__name__)
    # reprensentation
    def __repr__(self):
        representation=""
        if self.__dict__:
            # string standard data
            standardData=self.__dict__.copy()
            del standardData[IMAGE_MARKUP]
            representation=str(standardData)+linesep
            # string image
            rawIndex=0
            columnIndex=0
            pixelsNumber=self.width*self.height
            for pixelIndex in range(0,pixelsNumber):
                # add pixel related gradient
                pixelValue=self.image[pixelIndex]
                gradientIndex=int(pixelValue/REPRENSATION_INTERVAL)
                gradient=REPRENSATION_GRADIENT[gradientIndex]
                representation=representation+gradient
                # check if new new line
                if columnIndex<self.width-1:
                    columnIndex=columnIndex+1
                else:
                    representation=representation+linesep
                    columnIndex=0
                    rawIndex=rawIndex+1
            pass
        return representation
    def __str__(self):
        return self.__repr__()
    pass
# MINST data set extractor
class MinstDataSetExtractor():
    # extract data set
    def extractDataSet(self):
        # logger context
        argsStr = methodArgsStringRepresentation(signature(MinstDataSetExtractor.extractDataSet).parameters,locals())
        # logger input
        logger.loadedLogger.input(__name__, MinstDataSetExtractor.__name__, MinstDataSetExtractor.extractDataSet.__name__,message=argsStr)
        # parse labels file
        with open(self.labelsFileName, FileMode.BINARY.value) as labelsFile:
            # parse labels file header
            self.parseLabelsFileHeader(labelsFile)
            pass
        labelsFile.close()
        # logger output
        logger.loadedLogger.output(__name__, MinstDataSetExtractor.__name__, MinstDataSetExtractor.extractDataSet.__name__)
    # parse labels file header
    def parseLabelsFileHeader(self,labelsFile):
        # logger context
        argsStr = methodArgsStringRepresentation(signature(MinstDataSetExtractor.parseLabelsFileHeader).parameters,locals())
        # logger input
        logger.loadedLogger.input(__name__, MinstDataSetExtractor.__name__, MinstDataSetExtractor.parseLabelsFileHeader.__name__,message=argsStr)
        # get file size
        fileSize=stat(self.labelsFileName).st_size
        # parse labels file header
        for index in range(0, HeaderSize.LABEL.value):
            binaryValue = labelsFile.read(DataTypeSize.INTEGER_SIZE.value)
            numericValue = int.from_bytes(binaryValue, byteorder=ENDIAN)
            # control magik number
            if index == 0:
                magicNumber = numericValue
                if MagicNumber.LABEL.value != magicNumber:
                    errorMessage = "Labels magic number does not match : expected=" + str(MagicNumber.LABEL.value) + " actual=" + str(magicNumber)
                    logger.loadedLogger.error(__name__, MinstDataSetExtractor.__name__,MinstDataSetExtractor.parseLabelsFileHeader.__name__, errorMessage)
                    raise Exception(errorMessage)
            else:
                labelsNumber = numericValue
        # logger output
        logger.loadedLogger.output(__name__, MinstDataSetExtractor.__name__, MinstDataSetExtractor.parseLabelsFileHeader.__name__,labelsNumber)
        # return
        return labelsNumber
    # constructor
    def __init__(self, labelsFileName, imagesFileName, outputDirectoryName,patternValue):
        # logger context
        argsStr = methodArgsStringRepresentation(signature(MinstDataSetExtractor.__init__).parameters,locals())
        # logger input
        logger.loadedLogger.input(__name__, MinstDataSetExtractor.__name__, MinstDataSetExtractor.__init__.__name__,message=argsStr)
        # check patternValue
        patternValues=Pattern.listValues()
        if patternValue.upper() not in patternValues:
            errorMessage="Pattern does not match : expected=" + str(patternValues) + " actual=" + str(patternValue)
            logger.loadedLogger.error(__name__, MinstDataSetExtractor.__name__, MinstDataSetExtractor.__init__.__name__, errorMessage)
            raise Exception(errorMessage)
        # create output folder is needed
        if exists(outputDirectoryName):
            if not isdir(outputDirectoryName):
                errorMessage = "There is already something at output folder : " +outputDirectoryName
                logger.loadedLogger.error(__name__, MinstDataSetExtractor.__name__,MinstDataSetExtractor.__init__.__name__, errorMessage)
                raise Exception(errorMessage)
        else:
            makedirs(outputDirectoryName)
        # construct object
        self.labelsFileName=labelsFileName
        self.imagesFileName=imagesFileName
        self.patternValue=patternValue
        self.outputDirectoryName=outputDirectoryName
        # logger output
        logger.loadedLogger.output(__name__, MinstDataSetExtractor.__name__, MinstDataSetExtractor.__init__.__name__)
# run extractor
if __name__ == '__main__':
    # EXTRACT DATA SET
    labelsFileName="/mnt/hgfs/shared/Documents/myDevelopment/MNISTdataSetExtractor/UnarchivedDataSet/t10k-labels.idx1-ubyte"
    imagesFileName = "/mnt/hgfs/shared/Documents/myDevelopment/MNISTdataSetExtractor/UnarchivedDataSet/t10k-images.idx3-ubyte"
    patternValue=Pattern.TEST.value
    outputDirectoryName = "/mnt/hgfs/shared/Documents/myDevelopment/MNISTdataSetExtractor/ExtractedDataSet/"+patternValue
    mdse=MinstDataSetExtractor(labelsFileName, imagesFileName,outputDirectoryName,patternValue)
    mdse.extractDataSet()
    # CHECK EXTRACTED DATA
    #testData=TestData()
    #for i in range(0,10):
    #    testData.load("/mnt/hgfs/shared/Documents/myDevelopment/MNISTdataSetExtractor/ExtractedDataSet/TEST/"+str(i)+TEST_FILE_EXTENSION)
    #    print(str(testData))
    #    pass
    pass
pass
