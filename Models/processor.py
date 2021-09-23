import random, itertools, time
from cacheMemory import CacheMemory
from mainMemory import MainMemory
from memoryController import MemoryController
from bus import Bus

class Processor:

    processorCounter = itertools.count()
    
    def __init__(self):
        
        self.processorID = next(Processor.processorCounter)
        self.currentInstruction = []
        self.isProcessing = False
        self.isOn = False
        self.myL1Cache = CacheMemory()
        self.myMainMemory = MainMemory.getMemoryInstance()
        self.myMemoryController = MemoryController(self.processorID)

    def getProcessor(self): return self.processorID
    def getCurrentInstruction(self): return self.currentInstruction
    def getIsProcessing(self): return self.isProcessing
    def getIsOn(self): return self.isOn
    def getL1Cache(self): return self.myL1Cache
    def getMainMemory(self): return self.myMainMemory
    def getMemoryController(self): return self.myMemoryController

    
    def setCurrentInstruction(self, _currentInstruction):

        self.currentInstruction = _currentInstruction

    def setIsProcessing(self, _isProcessing):

        self.isProcessing = _isProcessing

    def setIsOn(self, _isOn):

        self.isOn = _isOn

    def runProcessor(self): return 0

    def stopProcessor(self): return 0

    def instructionGenerator(self):

        type = self.randomDist(2)
        currentInst = []

        if type == 0:
            memoryLocation = self.randomDist(7)
            currentInst.append("READ")
            currentInst.append(memoryLocation)
        
        elif type == 1:
            memoryLocation = self.randomDist(7)
            data = self.randomDist(65535)
            currentInst.append("WRITE")
            currentInst.append(memoryLocation)
            currentInst.append(data)


        else:
            currentInst.append("CALC")
        
        self.setCurrentInstruction(currentInst)


    def randomDist(self,maxNumber): return random.randint(0,maxNumber)

    def calcInstruction(self):

        print("Processor P{} is doing some calculations...".format(self.processorID))
        time.sleep(2.5)
        print("Processor P{} has finished the calculations...".format(self.processorID))

    def memoryInstruction(self):

        print("Processor P{} is executing some memory instruction...".format(self.processorID))
        currentInst = self.getCurrentInstruction()
        instructionType = currentInst[0]
        myL1Cache = self.getL1Cache()
        myMemoryController = self.getMemoryController()
        dirMem = currentInst[1]
        cacheDir = myMemoryController.getCacheBlock1_way(dirMem)
        validBit = myL1Cache.getCacheBlocks()[cacheDir][0]
        cacheTag = myL1Cache.getCacheBlocks()[cacheDir][1]

        if instructionType == "READ":

            if validBit == 1 and myMemoryController.checkCacheBlock(dirMem, cacheTag, cacheDir):
                print("READ HIT Processor P{}".format(self.getProcessor()))
                myMemoryController.addressingReadHit(cacheDir,dirMem, myL1Cache)

            else:
                print("READ MISS Processor P{}".format(self.getProcessor()))
                myMemoryController.addressingReadMiss(cacheDir, dirMem, myL1Cache, self.getMainMemory())



        else:

            if validBit == 1 and myMemoryController.checkCacheBlock(dirMem, cacheTag, cacheDir):
                print("WRITE HIT Processor P{}".format(self.getProcessor()))
                myMemoryController.addressingWriteHit(cacheDir, dirMem, myL1Cache, currentInst[2])

            else:

                print("WRITE MISS Processor P{}".format(self.getProcessor()))
                myMemoryController.addressingWriteMiss(cacheDir, dirMem, myL1Cache, self.getMainMemory(), currentInst[2])

        print("Processor P{} has finished the memory instruction...".format(self.processorID))





    def toStringCurrentInstruction(self):

        currentInst = self.currentInstruction

        if len(currentInst) == 3:
            
            print("P", self.processorID, ":", sep = '', end = " ") 
            print(currentInst[0], format(currentInst[1],'04b'), ";", format(currentInst[2],'016X'))

        elif len(currentInst) == 2:

            print("P", self.processorID, ":", sep = '', end = " ") 
            print(currentInst[0], format(currentInst[1],'04b'))

        elif len(currentInst) == 1:

            print("P", self.processorID, ":", sep = '', end = " ")
            print(currentInst[0])

        else:
            print("P{}: Instruction set empty!".format(self.processorID))



def mainProcessor():

    p0 = Processor()
    p1 = Processor()
    p2 = Processor()
    p3 = Processor()

    myBus = Bus.getBusInstance()
    myBus.setProcessorArray([p0,p1,p2,p3])

    print("*********************************************")
    p0.setCurrentInstruction(["READ", 6])
    p0.toStringCurrentInstruction()
    p0.memoryInstruction()
    p0.getMainMemory().toStringMemory()
    p0.getL1Cache().toStringCacheComplete()
    p0.getMemoryController().toStringDirectoryValues()

    print("*********************************************")
    
    p1.setCurrentInstruction(["READ", 6])
    p1.toStringCurrentInstruction()
    p1.memoryInstruction()
    p1.getMainMemory().toStringMemory()
    p1.getL1Cache().toStringCacheComplete()
    p1.getMemoryController().toStringDirectoryValues()

    print("*********************************************")
    p0.setCurrentInstruction(["WRITE", 6, 25000])
    p0.toStringCurrentInstruction()
    p0.memoryInstruction()
    p0.getMainMemory().toStringMemory()
    p0.getL1Cache().toStringCacheComplete()
    p0.getMemoryController().toStringDirectoryValues()

    print("*********************************************")
    
    p3.setCurrentInstruction(["WRITE", 6, 17430])
    p3.toStringCurrentInstruction()
    p3.memoryInstruction()
    p3.getMainMemory().toStringMemory()
    p3.getL1Cache().toStringCacheComplete()
    p3.getMemoryController().toStringDirectoryValues()

    print("********************************************")
    p0.getL1Cache().toStringCacheComplete()



 


if __name__ == "__main__":
    
    print("Processor class!")
    mainProcessor()