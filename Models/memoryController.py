from bus import Bus

class MemoryController:

    directory = [['U',0,0,0,0],['U',0,0,0,0],['U',0,0,0,0],['U',0,0,0,0],
    ['U',0,0,0,0],['U',0,0,0,0],['U',0,0,0,0],['U',0,0,0,0]]

    def __init__(self, _currentCPU):

        self.currentCPU = _currentCPU

    def getCurrentCPU(self):

        return self.currentCPU

    def getCacheBlock1_way(self, dirMem):

        return dirMem % 4

    def generateTag(self, dirMem):

        if dirMem <= 3:

            return 0

        else:

            return 1

    def checkCacheBlock(self, dirMem, cacheTag, cacheDir):

        finalCacheDir = format(cacheTag,'02b') + format(cacheDir,'02b')

        return format(dirMem,'04b') == finalCacheDir

    def updateDirectoryValue(self, dirMem, processorID, value):

        MemoryController.directory[dirMem][processorID + 1] = value

    def updateDirectoryState(self, dirMem, newState):

        MemoryController.directory[dirMem][0] = newState

    def getCurrentState(self, dirMem):

        return MemoryController.directory[dirMem][0]

    def addressingReadMiss(self, cacheDir, dirMem, cacheL1, _mainMemory):

        currentState = self.getCurrentState(dirMem)

        if currentState == 'U':

            self.readMissU(cacheDir, dirMem, cacheL1, _mainMemory)

        elif currentState == 'S':

            self.readMissS(cacheDir, dirMem, cacheL1, _mainMemory)

        else: # State = 'M/E'

            self.readMissME(cacheDir, dirMem, cacheL1, _mainMemory)

    def addressingWriteMiss(self, cacheDir, dirMem, cacheL1, _mainMemory, newData):

        currentState = self.getCurrentState(dirMem)

        if currentState == 'U':

            self.writeMissU(cacheDir, dirMem, cacheL1, _mainMemory, newData)

        elif currentState == 'S':

            self.writeMissS(cacheDir, dirMem, cacheL1, _mainMemory, newData)

        else: # State = 'M/E'

            self.writeMissME(cacheDir, dirMem, cacheL1, _mainMemory, newData)

    def addressingReadHit(self, cacheDir, dirMem, cacheL1):

        currentState = self.getCurrentState(dirMem)

        if currentState == 'U':

            print("There is no Read Hit for Uncached State")

        elif currentState == 'S':

            self.readHitS(cacheDir, cacheL1)

        else: # State = 'M/E'

            self.readHitME(cacheDir, cacheL1)

    def addressingWriteHit(self, cacheDir, dirMem, cacheL1, newData):

        currentState = self.getCurrentState(dirMem)

        if currentState == 'U':

            print("There is no write Hit for Uncached State")

        elif currentState == 'S':

            self.writeHitS(cacheDir, dirMem, cacheL1, newData)

        else: # State = 'M/E'

            self.writeHitME(cacheDir, cacheL1, newData)

    def addressingBlockReplace(self, oldDirMem, newData, _mainMemory):

        currentState = self.getCurrentState(oldDirMem)

        if currentState == 'U':

            print("There is no Block Replace for Uncached State")

        elif currentState == 'S':

            self.blockReplaceS(oldDirMem)

        else: # State = 'M/E'

            self.blockReplaceME(oldDirMem, newData, _mainMemory)

    def readMissU(self, cacheDir, dirMem, cacheL1, _mainMemory):

        memoryData = _mainMemory.getBlockData(dirMem)
        newTag = self.generateTag(dirMem)
        newCacheBlock = [1,newTag,memoryData]
        oldCacheBlock = cacheL1.getCacheBlocks()[cacheDir]
        cacheL1.getCacheBlocks()[cacheDir] = newCacheBlock
        self.updateDirectoryState(dirMem,'S')
        self.updateDirectoryValue(dirMem,self.getCurrentCPU(), 1)

        if oldCacheBlock[1] == newCacheBlock[1]:

            print("No Block Replace operation was needed")

        else:

            oldDirMem = int(format(oldCacheBlock[1], '02b') + format(cacheDir, '02b'),2)
            self.addressingBlockReplace(oldDirMem, oldCacheBlock[2], _mainMemory)

    def readMissS(self,cacheDir, dirMem, cacheL1, _mainMemory):

        memoryData = _mainMemory.getBlockData(dirMem)
        newTag = self.generateTag(dirMem)
        newCacheBlock = [1,newTag,memoryData]
        oldCacheBlock = cacheL1.getCacheBlocks()[cacheDir]
        cacheL1.getCacheBlocks()[cacheDir] = newCacheBlock
        self.updateDirectoryValue(dirMem,self.getCurrentCPU(), 1)

        if oldCacheBlock[1] == newCacheBlock[1]:

            print("No Block Replace operation was needed")

        else:
            
            oldDirMem = int(format(oldCacheBlock[1], '02b') + format(cacheDir, '02b'),2)
            self.addressingBlockReplace(oldDirMem,oldCacheBlock[2], _mainMemory)

    
    def readMissME(self,cacheDir, dirMem, cacheL1, _mainMemory):

        myBus = Bus.getBusInstance()
        cpuID = 0

        for data in MemoryController.directory[dirMem][1:]:
            if data == 1:
                break
            else:
                cpuID += 1

        oldData = myBus.fetchingData(cacheDir,cpuID)
        newTag = self.generateTag(dirMem)
        newCacheBlock = [1,newTag,oldData]
        oldCacheBlock = cacheL1.getCacheBlocks()[cacheDir]
        cacheL1.getCacheBlocks()[cacheDir] = newCacheBlock
        _mainMemory.updateMemory(dirMem, oldData)
        self.updateDirectoryState(dirMem,'S')
        self.updateDirectoryValue(dirMem,self.getCurrentCPU(), 1)

        if oldCacheBlock[1] == newCacheBlock[1]:

            print("No Block Replace operation was needed")

        else:

            oldDirMem = int(format(oldCacheBlock[1], '02b') + format(cacheDir, '02b'),2)
            self.addressingBlockReplace(oldDirMem, oldCacheBlock[2], _mainMemory)


    def writeMissU(self, cacheDir, dirMem, cacheL1, _mainMemory, newData):

        memoryData = _mainMemory.getBlockData(dirMem)
        memoryData = newData
        newTag = self.generateTag(dirMem)
        newCacheBlock = [1,newTag,memoryData]
        oldCacheBlock = cacheL1.getCacheBlocks()[cacheDir]
        cacheL1.getCacheBlocks()[cacheDir] = newCacheBlock
        self.updateDirectoryState(dirMem,'M/E')
        self.updateDirectoryValue(dirMem,self.getCurrentCPU(), 1)

        if oldCacheBlock[1] == newCacheBlock[1]:

            print("No Block Replace operation was needed")

        else:

            oldDirMem = int(format(oldCacheBlock[1], '02b') + format(cacheDir, '02b'),2)
            self.addressingBlockReplace(oldDirMem, oldCacheBlock[2], _mainMemory)

    def writeMissS(self, cacheDir, dirMem, cacheL1, _mainMemory, newData):

        memoryData = _mainMemory.getBlockData(dirMem)
        memoryData = newData
        newTag = self.generateTag(dirMem)
        newCacheBlock = [1,newTag,memoryData]
        oldCacheBlock = cacheL1.getCacheBlocks()[cacheDir]
        cacheL1.getCacheBlocks()[cacheDir] = newCacheBlock
        invalidateArray = self.generateInvalidateArray(dirMem)
        myBus = Bus.getBusInstance()
        myBus.invalidateProcessors(invalidateArray,cacheDir)
        MemoryController.directory[dirMem] = ['M/E',0,0,0,0]
        self.updateDirectoryValue(dirMem,self.getCurrentCPU(), 1)

        if oldCacheBlock[1] == newCacheBlock[1]:

            print("No Block Replace operation was needed")

        else:

            oldDirMem = int(format(oldCacheBlock[1], '02b') + format(cacheDir, '02b'),2)
            self.addressingBlockReplace(oldDirMem, oldCacheBlock[2], _mainMemory)

  
    def writeMissME(self, cacheDir, dirMem, cacheL1, _mainMemory, newData):
        
        myBus = Bus.getBusInstance()
        cpuID = 0

        for data in MemoryController.directory[dirMem][1:]:
            if data == 1:
                break
            else:
                cpuID += 1

        oldData = myBus.fetchingData(cacheDir,cpuID)
        invalidateArray = self.generateInvalidateArray(dirMem)
        myBus.invalidateProcessors(invalidateArray,cacheDir)
        newTag = self.generateTag(dirMem)
        newCacheBlock = [1,newTag,newData]
        oldCacheBlock = cacheL1.getCacheBlocks()[cacheDir]
        cacheL1.getCacheBlocks()[cacheDir] = newCacheBlock
        MemoryController.directory[dirMem] = ['M/E',0,0,0,0]
        self.updateDirectoryValue(dirMem,self.getCurrentCPU(), 1)

        if oldCacheBlock[1] == newCacheBlock[1]:

            print("No Block Replace operation was needed")

        else:

            oldDirMem = int(format(oldCacheBlock[1], '02b') + format(cacheDir, '02b'),2)
            self.addressingBlockReplace(oldDirMem, oldCacheBlock[2], _mainMemory)

        

    def readHitS(self, cacheDir, cacheL1):

        cacheBlock = cacheL1.getCacheBlocks()[cacheDir]
        print("Block readed: V = {}, Tag = {}, Data = {} ".format(cacheBlock[0], cacheBlock[1], hex(cacheBlock[2])))
        print("No Block Replace operation was needed")

    def readHitME(self, cacheDir, cacheL1):
        
        cacheBlock = cacheL1.getCacheBlocks()[cacheDir]
        print("Block readed: V = {}, Tag = {}, Data = {} ".format(cacheBlock[0], cacheBlock[1], hex(cacheBlock[2])))
        print("No Block Replace operation was needed")


    def writeHitS(self,cacheDir, dirMem, cacheL1, newData):
        
        if self.isOnly1CPU(dirMem):

            cacheL1.getCacheBlocks()[cacheDir][2] = newData
            self.updateDirectoryState(dirMem,'M/E')

        else:
            cacheL1.getCacheBlocks()[cacheDir][2] = newData
            invalidateArray = self.generateInvalidateArray(dirMem)
            myBus = Bus.getBusInstance()
            myBus.invalidateProcessors(invalidateArray,cacheDir)
            MemoryController.directory[dirMem] = ['M/E',0,0,0,0]
            self.updateDirectoryValue(dirMem,self.getCurrentCPU(), 1)

        print("No Block Replace operation was needed")

    def writeHitME(self, cacheDir, cacheL1, newData):

        cacheL1.getCacheBlocks()[cacheDir][2] = newData
        print("No Block Replace operation was needed")


    def blockReplaceS(self, dirMem):

        print("Block replace: Shared state")

        if self.isOnly1CPU(dirMem):

            newDirectoryBlock = ['U',0,0,0,0]
            MemoryController.directory[dirMem] = newDirectoryBlock

        else:

            self.updateDirectoryValue(dirMem,self.getCurrentCPU(),0)

    def blockReplaceME(self, oldDirMem, newData, _mainMemory):

        print("Block replace: Modified/Exclusive state")
        _mainMemory.updateMemory(oldDirMem, newData)
        newDirectoryBlock = ['U',0,0,0,0]
        MemoryController.directory[oldDirMem] = newDirectoryBlock


    def isOnly1CPU(self, dirMem):

        memBlock = MemoryController.directory[dirMem]
        dataF = 0

        for data in memBlock[1:]: dataF += data

        if dataF == 1:
            return True

        else:
            return False

    def generateInvalidateArray(self, dirMem):

        memBlock = MemoryController.directory[dirMem]
        counter = 0
        invalidateArray = []

        for data in memBlock[1:]:

            if data == 1:

                if counter == self.getCurrentCPU():
                    invalidateArray.append(0)
                    counter += 1
                
                else:

                    invalidateArray.append(1)
                    counter += 1

            else:

                invalidateArray.append(0)
                counter += 1

        return invalidateArray

    def toStringDirectoryValues(self):

        print("Directory Values: ")
        counter = 0

        for block in MemoryController.directory:

            print("Block {}: |".format(counter), end = " ")
            print("State: {} |".format(block[0]), end = " ")

            for bit in block[1:]:

                print(bit, "  |  ", end = "")

            print("")
            counter += 1

def mainMemoryController():

    memoryController1 = MemoryController(2)
    memoryController1.updateDirectoryValue(7,2,1)
    memoryController1.toStringDirectoryValues()
    print(memoryController1.checkCacheBlock(7,0,3))


if __name__ == "__main__":

    print("Memory Controller Class!")
    mainMemoryController()
        