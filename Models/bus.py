class Bus:

    _busInstance = None

    @staticmethod
    def getBusInstance():

        if Bus._busInstance == None:
            Bus()

        return Bus._busInstance

    def __init__(self):
        
        if Bus._busInstance != None:
            raise Exception("This class is a singleton and the constructor is private")

        else:
            Bus._busInstance = self
            self.myProcessorArray = []

    def getProcessorArray(self):

        return self.myProcessorArray

    def setProcessorArray(self, processorArray):

        self.myProcessorArray = processorArray
        
    def invalidateProcessors(self, invalidateArray, cacheDir):

        counter = 0
        
        for cpuID in invalidateArray:

            if cpuID == 0:
                counter += 1
                continue

            else:
                currentCPU = self.getProcessorArray()[counter]
                currentCPU.getL1Cache().getCacheBlocks()[cacheDir][0] = 0
                counter += 1

        print("Cache Blocks invalidate succesfully!")

    def fetchingData(self, cacheDir, cpuID):

        currentCPU = self.getProcessorArray()[cpuID]
        return currentCPU.getL1Cache().getCacheBlocks()[cacheDir][2]



if __name__== "__main__":
    
    print("Bus class!")