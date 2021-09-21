class MemoryController:

    directory = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

    def __init__(self, _currentCPU):

        self.currentCPU = _currentCPU

    def getCurrentCPU(self):

        return self.currentCPU

    def writeBackMemory(self, currentInstruction, myL1Cache, _mainMemory): return 0

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

    def updateDirectory(self, dirMem, processorID, value):

        MemoryController.directory[dirMem][processorID] = value

    def getCurrentState(self, cacheBlock): return 0

    def toStringDirectory(self):

        print("Directory Values: ")
        counter = 0

        for block in MemoryController.directory:

            print("Block {}: |".format(counter), end = " ")

            for bit in block:

                print(bit, "  |  ", end = "")

            print("")
            counter += 1

def mainMemoryController():

    memoryController1 = MemoryController(2)
    memoryController1.updateDirectory(7,2,1)
    memoryController1.toStringDirectory()
    print(memoryController1.checkCacheBlock(7,0,3))


if __name__ == "__main__":

    print("Memory Controller Class!")
    mainMemoryController()
        