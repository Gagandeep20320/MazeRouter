from typing import Collection
import numpy as np
import copy
from numpy.core.arrayprint import printoptions
# Wirelength in the wirelength matrix is one more than what it should be counted as
# Create individual traversal matrix and store them in list to finally sum them up
NUM_ROWS = 10
NUM_COLS = 10
NUM_LAY = 10
ROW_START = COL_START = LAY_START = 1


class traversalMat():
    def __init__(self):
        self.wirelength = 0
        self.pred = 'X'

    def printThisPoint(self):
        print("WL : ", self.wirelength)
        print("pred : ", self.pred)

    def incrementWirelengthBy(self, value):
        self.wirelength += value

    def initializeWirelength(self):
        self.wirelength = 0

    def initializePred(self):
        self.pred = 'X'


# traversalMatrix = np.full(
    # (NUM_ROWS + 1, NUM_COLS + 1, NUM_LAY + 1), traversalMat())
traversalMatrix = []


def create3DGrid(traversalMatt):
    dummyObj = traversalMat()
    traversalMatt = []
    for i in range(0, NUM_ROWS + 1):
        colList = []
        for j in range(0, NUM_COLS + 1):
            layList = []
            for k in range(0, NUM_LAY + 1):
                currGridPont = traversalMat()
                layList.append(currGridPont)
                # traversalMat[i][j][k].append(currGridPont)
            colList.append(layList[:])
        traversalMatt.append(colList[:])
    return copy.deepcopy(traversalMatt)


def initializeTraversalMatrix(traversalMat):
    for i in range(1, NUM_ROWS + 1):
        for j in range(1, NUM_COLS + 1):
            for k in range(1, NUM_LAY + 1):
                traversalMat[i][j][k].initializeWirelength()
                traversalMat[i][j][k].initializePred()


def printTraversalMatrixWL(traversalMat):
    for k in range(1, NUM_LAY + 1):
        print("Layer ", k)
        for i in range(1, NUM_ROWS + 1):
            for j in range(1, NUM_COLS + 1):
                print(traversalMat[i][j][k].wirelength, end=" ")
            print("\n")
        print("\n")


class Wirelength():
    

    def __init__(self):
        self.rowPosWf = []*1000
        self.colPosWf = []*1000
        self.layPosWf = []*1000
        pass

    def calculateWirelength(self, rStart, cStart, layStart, rEnd, cEnd, layEnd):
        initializeTraversalMatrix()
        self.findWirelengthCostAtAllGridPoints(
            rStart, cStart, layStart, rEnd, cEnd, layEnd)

    def findWirelengthCostAtAllGridPoints(self, rStart, cStart, layStart, rEnd, cEnd, layEnd):
        row = rStart
        col = cStart
        lay = layStart
        endReached = False
        if((row == rEnd) and (col == cEnd) and (lay == layEnd)):
            traversalMatrix[row][col][lay].wirelength = 1
            endReached = True
        else:
            traversalMatrix[row][col][lay].wirelength = 1
            endReached = self.getNeighbourForGivenCell(
                row, col, lay, rEnd, cEnd, layEnd)
            printTraversalMatrixWL(traversalMatrix)
            if(endReached == True):
                self.emptyQueues()
            while (endReached == False):
                # print(self.rowPosWf)
                row = self.rowPosWf[0]
                col = self.colPosWf[0]
                lay = self.layPosWf[0]
                self.rowPosWf.pop(0)
                self.colPosWf.pop(0)
                self.layPosWf.pop(0)
                endReached = self.getNeighbourForGivenCell(row,col,lay,rEnd,cEnd,layEnd)
                printTraversalMatrixWL(traversalMatrix)
                if(endReached == True):
                    self.emptyQueues()
                    break
        return endReached
    def getNeighbourForGivenCell(self, row, col, lay, rEnd, cEnd, layEnd):
        print("row, col, lay, rEnd, cEnd, layEnd = ", row,", ", col,", ", lay,", ", rEnd,", ", cEnd,", ", layEnd)
        destinationFound = False
        wirelengthCost = traversalMatrix[row][col][lay].wirelength + 1
        if(lay % 2 != 0):  # Odd layers allow movement only in columns
            print("Layer is odd")
            if(((col+1) <= NUM_COLS) and (traversalMatrix[row][col+1][lay].wirelength == 0)):
                traversalMatrix[row][col+1][lay].wirelength = wirelengthCost
                traversalMatrix[row][col+1][lay].pred = 'W'
                if((row == rEnd) and ((col+1) == cEnd) and (lay == layEnd)):
                    print("Destination towards east")
                    destinationFound = True
                    return destinationFound
                else:
                    self.rowPosWf.append(row)
                    self.colPosWf.append(col+1)
                    self.layPosWf.append(lay)

            if(((col-1) >= COL_START) and (traversalMatrix[row][col-1][lay].wirelength == 0)):

                traversalMatrix[row][col-1][lay].wirelength = wirelengthCost
                traversalMatrix[row][col-1][lay].pred = 'E'
                if((row == rEnd) and ((col-1) == cEnd) and (lay == layEnd)):
                    print("Destination towards West")
                    destinationFound = True
                    return destinationFound
                else:
                    self.rowPosWf.append(row)
                    self.colPosWf.append(col-1)
                    self.layPosWf.append(lay)
        else:  # Even Layers
            print("Layer is even")
            # Moving right prioritized
            if(((row+1) <= NUM_ROWS) and (traversalMatrix[row+1][col][lay].wirelength == 0)):
                traversalMatrix[row+1][col][lay].wirelength = wirelengthCost
                traversalMatrix[row+1][col][lay].pred = 'N'
                if(((row+1) == rEnd) and ((col) == cEnd) and (lay == layEnd)):
                    print("Destination towards south")
                    destinationFound = True
                    return destinationFound
                else:
                    self.rowPosWf.append(row+1)
                    self.colPosWf.append(col)
                    self.layPosWf.append(lay)
            # Moving right prioritized
            if(((row-1) >= ROW_START) and (traversalMatrix[row-1][col][lay].wirelength == 0)):
                traversalMatrix[row-1][col][lay].wirelength = wirelengthCost
                traversalMatrix[row-1][col][lay].pred = 'S'
                if(((row-1) == rEnd) and ((col) == cEnd) and (lay == layEnd)):
                    print("Destination towards north")
                    destinationFound = True
                    return destinationFound
                else:
                    self.rowPosWf.append(row-1)
                    self.colPosWf.append(col)
                    self.layPosWf.append(lay)
        # Moving right prioritized
        if(((lay+1) <= NUM_LAY) and (traversalMatrix[row][col][lay+1].wirelength == 0)):
            traversalMatrix[row][col][lay+1].wirelength = wirelengthCost
            traversalMatrix[row][col][lay+1].pred = 'D'
            if(((row) == rEnd) and ((col) == cEnd) and ((lay+1) == layEnd)):
                print("Via Upwards")
                destinationFound = True
                return destinationFound
            else:
                self.rowPosWf.append(row)
                self.colPosWf.append(col)
                self.layPosWf.append(lay+1)
        # Moving right prioritized
        print("lay - 1 = ", lay-1 )
        if(((lay-1) >= LAY_START) and (traversalMatrix[row][col][lay-1].wirelength == 0)):
            # print("Inserting via")
            traversalMatrix[row][col][lay-1].wirelength = wirelengthCost
            traversalMatrix[row][col][lay-1].pred = 'U'
            if(((row) == rEnd) and ((col) == cEnd) and ((lay-1) == layEnd)):
                print("Via downwards")
                destinationFound = True
                return destinationFound
            else:
                self.rowPosWf.append(row)
                self.colPosWf.append(col)
                self.layPosWf.append(lay-1)
        print("Didn't found the location")
        return destinationFound

    def emptyQueues(self):
        while (len(self.rowPosWf) != 0):
            row = self.rowPosWf[0]
            col = self.colPosWf[0]
            lay = self.layPosWf[0]
            catchTrue = self.updateNbForGivenCell(row, col, lay)
            self.rowPosWf.pop(0)
            self.colPosWf.pop(0)
            self.layPosWf.pop(0)

    def updateNbForGivenCell(self, row, col, lay):
        destinationFound = True
        wirelengthCost = traversalMatrix[row][col][lay].wirelength + 1
        if(lay % 2 != 0):  # Odd layers allow movement only in columns
            if(((col+1) <= NUM_COLS) and (traversalMatrix[row][col+1][lay].wirelength == 0)):
                traversalMatrix[row][col+1][lay].wirelength = wirelengthCost
            
            if(((col-1) >= COL_START) and (traversalMatrix[row][col-1][lay].wirelength == 0)):
                traversalMatrix[row][col-1][lay].wirelength = wirelengthCost
        else:  # Even Layers
            print("Layer is even")
            # Moving right prioritized
            if(((row+1) <= NUM_ROWS) and (traversalMatrix[row+1][col][lay].wirelength == 0)):
                traversalMatrix[row+1][col][lay].wirelength = wirelengthCost
            # Moving right prioritized
            if(((row-1) <= NUM_ROWS) and (traversalMatrix[row-1][col][lay].wirelength == 0)):
                traversalMatrix[row-1][col][lay].wirelength = wirelengthCost
        # Moving right prioritized
        if(((lay+1) <= NUM_LAY) and (traversalMatrix[row][col][lay+1].wirelength == 0)):
            traversalMatrix[row][col][lay+1].wirelength = wirelengthCost
        # Moving right prioritized
        if(((lay-1) <= LAY_START) and (traversalMatrix[row][col][lay-1].wirelength == 0)):
            traversalMatrix[row][col][lay-1].wirelength = wirelengthCost
        print("Didn't found the location")
        return destinationFound


wirelengthCalcObject = Wirelength()  # For testing
traversalMatrix = []
traversalMatrix = create3DGrid(traversalMatrix)
initializeTraversalMatrix(traversalMatrix)

print(wirelengthCalcObject.findWirelengthCostAtAllGridPoints(1, 1, 1, 10, 1, 1))
# printTraversalMatrixWL(traversalMatrix)


'''
! TODO
1. Retrive data (cell positions from the ML vector)
2. Calculate the total wirelength from all the cells
3. The challenge : What if two cells have same net being routed ? (Does that need to be routed if it is overlapping)
'''