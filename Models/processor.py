import random, itertools, time
from cacheMemory import CacheMemory
from mainMemory import MainMemory

class Processor:

    processorCounter = itertools.count()
    
    def __init__(self):
        
        self.processorID = next(Processor.processorCounter)
        self.currentInstruction = []
        self.isProcessing = False
        self.isOn = False
        self.myL1Cache = CacheMemory()
        self.myMainMemory = MainMemory.getMemoryInstance()

    def getProcessor(self): return self.processorID
    def getCurrentInstruction(self): return self.currentInstruction
    def getIsProcessing(self): return self.isProcessing
    def getIsOn(self): return self.isOn
    def getL1Cache(self): return self.myL1Cache
    def getMainMemory(self): return self.myMainMemory
    
    #def getMemoryController():

    
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
            currentInst.append(bin(memoryLocation))
        
        elif type == 1:
            memoryLocation = self.randomDist(7)
            data = self.randomDist(65535)
            currentInst.append("WRITE")
            currentInst.append(bin(memoryLocation))
            currentInst.append(hex(data))


        else:
            currentInst.append("CALC")
        
        self.setCurrentInstruction(currentInst)


    def randomDist(maxNumber): return random.randint(0,maxNumber)

    def calcInstruction(self):

        print("Processor P{} is doing some calculations...".format(self.processorID))
        time.sleep(2.5)
        print("Processor P{} has finished the calculations...".format(self.processorID))

    def memoryInstruction(self): return 0

    def toStringCurrentInstruction(self):

        currentInst = self.currentInstruction

        if len(currentInst) == 3:
            
            print("P", self.processorID, ":", sep = '', end = " ") 
            print(currentInst[0], format(currentInst[1],'b'), ";", format(currentInst[2],'X'))

        elif len(currentInst) == 2:

            print("P", self.processorID, ":", sep = '', end = " ") 
            print(currentInst[0], format(currentInst[1],'b'))

        else:

            print("P", self.processorID, ":", sep = '', end = " ")
            print(currentInst[0])



def mainProcessor():

    p0 = Processor()
    p1 = Processor()
    p0.getMainMemory().updateMemory(2,3)
    p1.getMainMemory().toStringMemory()


if __name__ == "__main__":
    
    print("Processor class!")
    mainProcessor()