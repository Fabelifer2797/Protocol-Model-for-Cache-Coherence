
class CacheMemory:

    def __init__(self):

        self.cacheBlocks = [0,0,0,0]

    def getCacheBlocks(self):

        return self.cacheBlocks

    def updateCacheBlock(self, blockNumber, data):

        self.cacheBlocks[blockNumber] = data

    def toStringCache(self):
        print("Cache Blocks:")
        print("    {}    |    {}    |    {}    |    {}   "
        .format(self.cacheBlocks[0], self.cacheBlocks[1], self.cacheBlocks[2], self.cacheBlocks[3]))


    
def mainCacheMemory():

    cache1 = CacheMemory()
    cache1.updateCacheBlock(2,5)
    cache1.updateCacheBlock(1,7)
    cache1.toStringCache()


if __name__ == "__main__":
    print("Cache memory Class!")
    mainCacheMemory()