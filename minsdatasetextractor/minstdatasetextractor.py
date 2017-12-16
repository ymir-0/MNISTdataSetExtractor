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
FILE_MODE="rb"
ENDIAN="big"
REPRENSATION_INTERVAL=51.2 # we have 256 grey level and 5 gradient char. 256/5=51.2
REPRENSATION_GRADIENT=(" ","░","▒","▓","█")
# load configuration
configurationLoader.loadConfiguration( CONFIGURATION_FILE )
logger.loadLogger("MinstDataSetExtractor",CONFIGURATION_FILE)
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
    def __init__(self, width=0, height=0, images=None, labels=None,pattern=None):
        # logger context
        argsStr = methodArgsStringRepresentation(signature(TestData.__init__).parameters,locals())
        # logger input
        logger.loadedLogger.input(__name__, TestData.__name__, TestData.__init__.__name__,message=argsStr)
        # construct object
        self.width = width
        self.height = height
        self.images = images
        self.labels = labels
        self.pattern = pattern
        # logger output
        logger.loadedLogger.output(__name__, TestData.__name__, TestData.__init__.__name__)
    def load(self, fileName):
        # logger context
        argsStr = methodArgsStringRepresentation(signature(TestData.__init__).parameters, locals())
        # logger input
        logger.loadedLogger.input(__name__, TestData.__name__, TestData.__init__.__name__, message=argsStr)
        # construct object
        file = open(fileName, "r")
        jsonTestData=file.read()
        file.close()
        loadedDict = loads(jsonTestData)
        self.__dict__.update(loadedDict)
        # logger output
        logger.loadedLogger.output(__name__, TestData.__name__, TestData.__init__.__name__)
    # reprensentation
    def __repr__(self):
        representation="None"
        if self.__dict__:
            # string standard data
            representation=str({"labels":self.labels,"pattern":self.pattern,"width":self.width,"height":self.height})+linesep
            # string image
            columnIndex=0
            for pixelIndex in range(0,self.width*self.height):
                # add pixel related gradient
                pixelValue=self.images[pixelIndex]
                gradientIndex=int(pixelValue/REPRENSATION_INTERVAL)
                gradient=REPRENSATION_GRADIENT[gradientIndex]
                representation=representation+gradient
                # check if new new line
                if columnIndex<self.width:
                    columnIndex=columnIndex+1
                else:
                    representation=representation+linesep
                    columnIndex=0
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
        # extract separated data
        labels=self.extractLabels()
        self.width, self.height, images = self.extractImages()
        # check size consistancy labels / images
        if len(labels)!=len(images):
            errorMessage="Size between labels & images does not match : labels=" + str(len(labels)) + " images=" + str(len(images))
            logger.loadedLogger.error(__name__, MinstDataSetExtractor.__name__, MinstDataSetExtractor.extractDataSet.__name__, errorMessage)
            raise Exception(errorMessage)
        # write data
        self.writeData(images ,labels)
        # logger output
        logger.loadedLogger.output(__name__, MinstDataSetExtractor.__name__, MinstDataSetExtractor.extractDataSet.__name__)
    # extract labels
    def extractLabels(self):
        # logger context
        argsStr = methodArgsStringRepresentation(signature(MinstDataSetExtractor.extractLabels).parameters,locals())
        # logger input
        logger.loadedLogger.input(__name__, MinstDataSetExtractor.__name__, MinstDataSetExtractor.extractLabels.__name__,message=argsStr)
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
            while index<labelsNumber:
                binaryValue = labelsFile.read(DataTypeSize.BYTE_SIZE.value)
                numericValue=int.from_bytes(binaryValue, byteorder=ENDIAN)
                labels[index]=str(numericValue)
                index=index+1
            labelsFile.close()
        # logger output
        logger.loadedLogger.output(__name__, MinstDataSetExtractor.__name__, MinstDataSetExtractor.extractLabels.__name__,labels)
        # return
        return labels
    # check labels file
    def checkLabelsFile(self,fileSize,magicNumber,labelsNumber):
        # logger context
        argsStr = methodArgsStringRepresentation(signature(MinstDataSetExtractor.checkLabelsFile).parameters,locals())
        # logger input
        logger.loadedLogger.input(__name__, MinstDataSetExtractor.__name__, MinstDataSetExtractor.checkLabelsFile.__name__,message=argsStr)
        # check magic number
        if MagicNumber.LABEL.value != magicNumber:
            errorMessage="Labels magic number does not match : expected=" + str(MagicNumber.LABEL.value) + " actual="+str(magicNumber)
            logger.loadedLogger.error(__name__, MinstDataSetExtractor.__name__, MinstDataSetExtractor.checkLabelsFile.__name__, errorMessage)
            raise Exception(errorMessage)
        # check size
        expectedSize=labelsNumber+(HeaderSize.LABEL.value*DataTypeSize.INTEGER_SIZE.value)
        if expectedSize != fileSize:
            errorMessage="Labels file size does not match : expected=" + str(expectedSize) + " actual="+str(fileSize)
            logger.loadedLogger.error(__name__, MinstDataSetExtractor.__name__, MinstDataSetExtractor.checkLabelsFile.__name__, errorMessage)
            raise Exception(errorMessage)
        # logger output
        logger.loadedLogger.output(__name__, MinstDataSetExtractor.__name__, MinstDataSetExtractor.checkLabelsFile.__name__)
    # extract images
    def extractImages(self):
        # logger context
        argsStr = methodArgsStringRepresentation(signature(MinstDataSetExtractor.extractImages).parameters,locals())
        # logger input
        logger.loadedLogger.input(__name__, MinstDataSetExtractor.__name__, MinstDataSetExtractor.extractImages.__name__,message=argsStr)
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
                    width = numericValue
                else:
                    height = numericValue
                    pixelNumbers = width * height
                    self.checkImagesFile(fileSize, magicNumber, imagesNumber,pixelNumbers)
            # read body
            images=dict()
            pixels=list()
            imageIndex=0
            pixelIndex=0
            while imageIndex<imagesNumber:
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
        # logger output
        logger.loadedLogger.output(__name__, MinstDataSetExtractor.__name__, MinstDataSetExtractor.extractImages.__name__,(width , height, images))
        # return
        return width , height, images
    # check images file
    def checkImagesFile(self,fileSize,magicNumber,imagesNumber,pixelNumbers):
        # logger context
        argsStr = methodArgsStringRepresentation(signature(MinstDataSetExtractor.checkImagesFile).parameters,locals())
        # logger input
        logger.loadedLogger.input(__name__, MinstDataSetExtractor.__name__, MinstDataSetExtractor.checkImagesFile.__name__,message=argsStr)
        # check magic number
        if MagicNumber.IMAGE.value != magicNumber:
            errorMessage="Images magic number does not match : expected=" + str(MagicNumber.IMAGE.value) + " actual="+str(magicNumber)
            logger.loadedLogger.error(__name__, MinstDataSetExtractor.__name__, MinstDataSetExtractor.checkImagesFile.__name__, errorMessage)
            raise Exception(errorMessage)
        # check size
        expectedSize=(imagesNumber*pixelNumbers)+(HeaderSize.IMAGE.value*DataTypeSize.INTEGER_SIZE.value)
        if expectedSize != fileSize:
            errorMessage="Images file size does not match : expected=" + str(expectedSize) + " actual="+str(fileSize)
            logger.loadedLogger.error(__name__, MinstDataSetExtractor.__name__, MinstDataSetExtractor.checkImagesFile.__name__, errorMessage)
            raise Exception(errorMessage)
        # logger output
        logger.loadedLogger.output(__name__, MinstDataSetExtractor.__name__, MinstDataSetExtractor.checkImagesFile.__name__)
    # write data
    def writeData(self, images, labels):
        # logger context
        argsStr = methodArgsStringRepresentation(signature(MinstDataSetExtractor.writeData).parameters,locals())
        # logger input
        logger.loadedLogger.input(__name__, MinstDataSetExtractor.__name__, MinstDataSetExtractor.writeData.__name__,message=argsStr)
        # for each test data
        for index in range(0, len(images)):
            # encode it
            objectTestData=TestData(self.width, self.height, images[index], labels[index],self.patternValue)
            dictTestData=dumps(objectTestData.__dict__)
            # write it into file
            testFileName=join(self.outputDirectoryName,str(index)+".json")
            testFile = open(testFileName, "w")
            testFile.write(dictTestData)
            testFile.close()
        # logger output
        logger.loadedLogger.output(__name__, MinstDataSetExtractor.__name__, MinstDataSetExtractor.writeData.__name__)
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
    #labelsFileName="/mnt/hgfs/shared/Documents/myDevelopment/MNISTdataSetExtractor/UnarchivedDataSet/t10k-labels.idx1-ubyte"
    #imagesFileName = "/mnt/hgfs/shared/Documents/myDevelopment/MNISTdataSetExtractor/UnarchivedDataSet/t10k-images.idx3-ubyte"
    #patternValue=Pattern.TEST.value
    #outputDirectoryName = "/mnt/hgfs/shared/Documents/myDevelopment/MNISTdataSetExtractor/ExtractedDataSet/"+patternValue
    #mdse=MinstDataSetExtractor(labelsFileName, imagesFileName,outputDirectoryName,patternValue)
    #mdse.extractDataSet()
    # CHECK EXTRACTED DATA
    testData=TestData()
    testData.load("/mnt/hgfs/shared/Documents/myDevelopment/MNISTdataSetExtractor/ExtractedDataSet/TEST/0.json")
    print(str(testData))
    pass
pass
