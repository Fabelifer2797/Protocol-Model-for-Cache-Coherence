import sys
from Models.processor import Processor
from Models.bus import Bus
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QScrollArea


class ApplicationScreen(QDialog):
    def __init__(self):
        super(ApplicationScreen,self).__init__()
        loadUi("multiCoreSystem.ui",self)
        self.setColumnWidthTables()
        self.setRowCountTables()


    def setColumnWidthTables(self):
        self.iTable0.setColumnWidth(0,300)
        self.iTable0.setColumnWidth(1,300)
        self.iTable1.setColumnWidth(0,300)
        self.iTable1.setColumnWidth(1,300)
        self.iTable2.setColumnWidth(0,300)
        self.iTable2.setColumnWidth(1,300)
        self.iTable3.setColumnWidth(0,300)
        self.iTable3.setColumnWidth(1,300)
        self.cache0.setColumnWidth(0,100)
        self.cache0.setColumnWidth(1,100)
        self.cache0.setColumnWidth(2,100)
        self.cache0.setColumnWidth(3,300)
        self.cache1.setColumnWidth(0,100)
        self.cache1.setColumnWidth(1,100)
        self.cache1.setColumnWidth(2,100)
        self.cache1.setColumnWidth(3,300)
        self.cache2.setColumnWidth(0,100)
        self.cache2.setColumnWidth(1,100)
        self.cache2.setColumnWidth(2,100)
        self.cache2.setColumnWidth(3,300)
        self.cache3.setColumnWidth(0,100)
        self.cache3.setColumnWidth(1,100)
        self.cache3.setColumnWidth(2,100)
        self.cache3.setColumnWidth(3,300)
        self.memoryTable.setColumnWidth(0,200)
        self.memoryTable.setColumnWidth(1,400)
        self.directoryTable.setColumnWidth(0,100)
        self.directoryTable.setColumnWidth(1,100)
        self.directoryTable.setColumnWidth(2,100)
        self.directoryTable.setColumnWidth(3,100)
        self.directoryTable.setColumnWidth(4,100)
        self.directoryTable.setColumnWidth(5,100)

    def setRowCountTables(self):
        
        self.iTable0.setRowCount(1)
        self.iTable1.setRowCount(1)
        self.iTable2.setRowCount(1)
        self.iTable3.setRowCount(1)
        self.cache0.setRowCount(4)
        self.cache1.setRowCount(4)
        self.cache2.setRowCount(4)
        self.cache3.setRowCount(4)
        self.memoryTable.setRowCount(8)
        self.directoryTable.setRowCount(8)


    def loadDataITable(self, cpuID, printData):

        if cpuID == 0:
            self.iTable0.setItem(0,0,QtWidgets.QTableWidgetItem(printData[0]))
            self.iTable0.setItem(0,1,QtWidgets.QTableWidgetItem(printData[1]))

        elif cpuID == 1:
            self.iTable1.setItem(0,0,QtWidgets.QTableWidgetItem(printData[0]))
            self.iTable1.setItem(0,1,QtWidgets.QTableWidgetItem(printData[1]))

        elif cpuID == 2:
            self.iTable2.setItem(0,0,QtWidgets.QTableWidgetItem(printData[0]))
            self.iTable2.setItem(0,1,QtWidgets.QTableWidgetItem(printData[1]))

        else:
            self.iTable3.setItem(0,0,QtWidgets.QTableWidgetItem(printData[0]))
            self.iTable3.setItem(0,1,QtWidgets.QTableWidgetItem(printData[1]))

    def loadDataCacheTable(self, cpuID, printData):

        if cpuID == 0:
            for i in range(4):
                for j in range(4):
                    self.cache0.setItem(i,j,QtWidgets.QTableWidgetItem(printData[i][j]))


        elif cpuID == 1:
            for i in range(4):
                for j in range(4):
                    self.cache1.setItem(i,j,QtWidgets.QTableWidgetItem(printData[i][j]))

        elif cpuID == 2:
            for i in range(4):
                for j in range(4):
                    self.cache2.setItem(i,j,QtWidgets.QTableWidgetItem(printData[i][j]))

        else:
            for i in range(4):
                for j in range(4):
                    self.cache3.setItem(i,j,QtWidgets.QTableWidgetItem(printData[i][j]))

    def loadDataMemoryTable(self, printData):

        for i in range(8):
            for j in range(2):
                self.memoryTable.setItem(i,j,QtWidgets.QTableWidgetItem(printData[i][j]))


    def loadDatadirectoryTable(self, printData):

        for i in range(8):
            for j in range(6):
                self.directoryTable.setItem(i,j,QtWidgets.QTableWidgetItem(printData[i][j]))

def mainGUI():

    app = QApplication(sys.argv)
    GUI = ApplicationScreen()
    scroll = QScrollArea()
    scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    scroll.setWidget(GUI)
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(scroll)
    widget.setWindowTitle("Protocol for Cache Coherence")
    widget.showMaximized() 

    p0 = Processor(3,GUI)
    p1 = Processor(3,GUI)
    p2 = Processor(3,GUI)
    p3 = Processor(3,GUI)
    threadArray = [p0,p1,p2,p3]
    systemBUs = Bus.getBusInstance()
    systemBUs.setProcessorArray(threadArray)
    p0.start()
    p1.start()
    p2.start()
    p3.start()


    sys.exit(app.exec())



if __name__ == "__main__":
    
    mainGUI()