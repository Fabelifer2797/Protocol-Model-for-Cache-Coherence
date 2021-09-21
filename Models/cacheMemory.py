
class CacheMemory:

    def __init__(self):

        self.cacheBlocks = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]

    def getCacheBlocks(self):

        return self.cacheBlocks

    def updateCacheBlockData(self, blockNumber, data):

        self.cacheBlocks[blockNumber][2] = data

    def updateValidBit(self, blockNumber, value):

        self.cacheBlocks[blockNumber][0] = value

    def updateTag(self, blockNumber, tagValue):

        self.cacheBlocks[blockNumber][1] = tagValue

    def toStringCacheData(self):
        print("Cache Blocks:")

        for data in self.cacheBlocks:
            
            print(format(data[2],'X'), "  |  ", end = "")

        print("")

    def toStringCacheComplete(self):

        print("Cache Blocks:")

        for data in self.cacheBlocks:

            print(format(data[0],'b'), "  |  ", format(data[1],'b'), "  |  ", format(data[2],'X'), "  ||  ",
            end = "")
        
        print("")
    
def mainCacheMemory():

    cache1 = CacheMemory()
    cache1.updateCacheBlockData(2,123)
    cache1.updateCacheBlockData(1,345)
    cache1.updateValidBit(1,1)
    cache1.updateTag(1, 1)
    cache1.toStringCacheComplete()


if __name__ == "__main__":
    print("Cache memory Class!")
    mainCacheMemory()