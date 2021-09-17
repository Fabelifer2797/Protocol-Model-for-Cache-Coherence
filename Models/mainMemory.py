class MainMemory:

    _memoryInstance = None

    @staticmethod
    def getMemoryInstance():

        if MainMemory._memoryInstance == None:
            MainMemory()
        
        return MainMemory._memoryInstance


    def __init__(self):
        
        if MainMemory._memoryInstance != None:
            raise Exception("This class is a singleton and the constructor is private")

        else:
            MainMemory._memoryInstance = self
            self.memoryBlocks = [0,0,0,0,0,0,0,0]

    def getMemoryBlocks(self):

        return self.memoryBlocks

    def updateMemory(self, blockNumber, data):

        self.memoryBlocks[blockNumber] = data

    def toStringMemory(self):
        print("Memory Blocks:")

        for data in self.memoryBlocks:
            print(data,"  |  ", end = "")

        print("\n")    

def mainMemory():
    
    memory1 = MainMemory.getMemoryInstance()
    memory1.updateMemory(3,7)
    memory2 = MainMemory.getMemoryInstance()
    memory2.toStringMemory()


if __name__ == "__main__":
    print("Main Memory Class!")
    mainMemory()