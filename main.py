from Models.processor import Processor
from Models.bus import Bus



def systemMain():

    p0 = Processor(10)
    p1 = Processor(10)
    p2 = Processor(10)
    p3 = Processor(10)
    systemBUs = Bus.getBusInstance()
    systemBUs.setProcessorArray([p0,p1,p2,p3])
    p0.start()
    p1.start()
    p2.start()
    p3.start()
    p0.join()
    p1.join()
    p2.join()
    p3.join()


if __name__ == "__main__":
    print("Init Multiprocessor System")
    systemMain()