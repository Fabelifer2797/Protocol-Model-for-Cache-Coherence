import random, itertools, time
import threading
from Models.cacheMemory import CacheMemory
from Models.mainMemory import MainMemory
from Models.memoryController import MemoryController
from Models.bus import Bus
import numpy as np

threadLock = threading.Lock()
threadLock2 = threading.Lock()

class Processor(threading.Thread):

    processorCounter = itertools.count()
    
    def __init__(self, _GUI):
        threading.Thread.__init__(self)
        self.processorID = next(Processor.processorCounter)
        self.currentInstruction = []
        self.previousInstrcution = []
        self.myL1Cache = CacheMemory()
        self.myMainMemory = MainMemory.getMemoryInstance()
        self.myMemoryController = MemoryController(self.processorID)
        self.GUI = _GUI


    def getProcessor(self): return self.processorID
    def getMaxIteration(self): return self.maxIteration
    def getCurrentInstruction(self): return self.currentInstruction
    def getL1Cache(self): return self.myL1Cache
    def getMainMemory(self): return self.myMainMemory
    def getMemoryController(self): return self.myMemoryController

    
    def setCurrentInstruction(self, _currentInstruction):

        self.currentInstruction = _currentInstruction


    # Override function run() of Thread Class
    def run(self):

        while True:
            
            self.run2()
            time.sleep(10)    
        
            
    def run2(self):

        threadLock2.acquire()
        currentInst = []
        
        
        if self.GUI.systemOn:
            
            print("System on... P{}".format(self.getProcessor()))

            if self.GUI.manualMode and self.GUI.currentCPU == self.getProcessor():
                self.GUI.manualMode = False
                self.GUI.currentCPU = -1
                currentInst = self.getCurrentInstruction()

            else:
                                
                self.instructionGenerator()
                currentInst = self.getCurrentInstruction()
            
            
            if currentInst[0] == "CALC":
                self.calcInstruction()
                self.displayInformation()
            
            else:
                self.memoryInstruction()
                self.displayInformation()

            

        else:
            print("System off... P{}".format(self.getProcessor()))

            if self.GUI.manualMode and self.GUI.currentCPU == self.getProcessor():
                
                self.previousInstrcution = self.currentInstruction
                self.setCurrentInstruction(self.GUI.currentInstruction)
                print("Instruction inserted in P{}".format(self.getProcessor()))
                self.GUI.systemOn = True
        
        threadLock2.release()

                

    def displayInformation(self):
        threadLock.acquire()
        currentInst = self.toStringCurrentInstruction()
        previousInst = self.toStringPreviousInstruction()
        self.GUI.loadDataITable(self.getProcessor(), [previousInst,currentInst])
        printCache = self.getL1Cache().getPrintCache()
        self.GUI.loadDataCacheTable(self.getProcessor(), printCache)
        printMemory = self.getMainMemory().getPrintMemory()
        self.GUI.loadDataMemoryTable(printMemory)
        printDirectory = self.getMemoryController().getPrintDirectory()
        self.GUI.loadDatadirectoryTable(printDirectory)
        threadLock.release()

    def stopProcessor(self): return 0

    def instructionGenerator(self):

        self.previousInstrcution = self.currentInstruction
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


    def randomDist(self,maxNumber): 
        
        random = -1

        while random < 0 or random > maxNumber:
            random = np.random.poisson(maxNumber)

        return round(random)

    def calcInstruction(self):

        #print("Processor P{} is doing some calculations...".format(self.processorID))
        time.sleep(2)
        #print("Processor P{} has finished the calculations...".format(self.processorID))

    def memoryInstruction(self):

        #print("Processor P{} is executing some memory instruction...".format(self.processorID))
        currentInst = self.getCurrentInstruction()
        instructionType = currentInst[0]
        myMemoryController = self.getMemoryController()
        dirMem = currentInst[1]
        cacheDir = myMemoryController.getCacheBlock1_way(dirMem)
        threadLock.acquire()
        myL1Cache = self.getL1Cache()
        validBit = myL1Cache.getCacheBlocks()[cacheDir][0]
        cacheTag = myL1Cache.getCacheBlocks()[cacheDir][1]

        if instructionType == "READ":

            if validBit == 1 and myMemoryController.checkCacheBlock(dirMem, cacheTag, cacheDir):
                #print("READ HIT Processor P{}".format(self.getProcessor()))
                myMemoryController.addressingReadHit(cacheDir,dirMem, myL1Cache)

            else:
                #print("READ MISS Processor P{}".format(self.getProcessor()))
                myMemoryController.addressingReadMiss(cacheDir, dirMem, myL1Cache, self.getMainMemory())



        else:

            if validBit == 1 and myMemoryController.checkCacheBlock(dirMem, cacheTag, cacheDir):
                #print("WRITE HIT Processor P{}".format(self.getProcessor()))
                myMemoryController.addressingWriteHit(cacheDir, dirMem, myL1Cache, currentInst[2])

            else:

                #print("WRITE MISS Processor P{}".format(self.getProcessor()))
                myMemoryController.addressingWriteMiss(cacheDir, dirMem, myL1Cache, self.getMainMemory(), currentInst[2])

        threadLock.release()
        time.sleep(4)
        #print("Processor P{} has finished the memory instruction...".format(self.processorID))





    def toStringCurrentInstruction(self):

        currentInst = self.currentInstruction

        if len(currentInst) == 3:
            
            print("P", self.processorID, ":", sep = '', end = " ") 
            print(currentInst[0], format(currentInst[1],'04b'), ";", format(currentInst[2],'016X'))
            return "P{}: {} {:04b}, {:016X}".format(self.processorID, currentInst[0], currentInst[1], currentInst[2])

        elif len(currentInst) == 2:

            print("P", self.processorID, ":", sep = '', end = " ") 
            print(currentInst[0], format(currentInst[1],'04b'))
            return "P{}: {} {:04b}".format(self.processorID, currentInst[0], currentInst[1])

        elif len(currentInst) == 1:

            print("P", self.processorID, ":", sep = '', end = " ")
            print(currentInst[0])
            return "P{}: {}".format(self.processorID, currentInst[0])

        else:
            print("P{}: Instruction set empty!".format(self.processorID))
            return "P{}: STALL".format(self.processorID)

    def toStringPreviousInstruction(self):

        previousInst = self.previousInstrcution

        if len(previousInst) == 3:
            return "P{}: {} {:04b}, {:016X}".format(self.processorID, previousInst[0], previousInst[1], previousInst[2])

        elif len(previousInst) == 2:
            return "P{}: {} {:04b}".format(self.processorID, previousInst[0], previousInst[1])

        elif len(previousInst) == 1:
            return "P{}: {}".format(self.processorID, previousInst[0])

        else:
            return "P{}: STALL".format(self.processorID)



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