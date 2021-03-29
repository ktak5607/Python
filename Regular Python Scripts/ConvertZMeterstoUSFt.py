import os
import re
from decimal import*

#Convert to State Plane Coordinates
def ConvToSF():
    intCoordFile = open (outCoordFile, 'a')

    for line in coordFile:
        numList = re.sub(" ", " ", line).split()
        scaleFactor = 3.280833333333
        xCoord = Decimal(numList[0])
        yCoord = Decimal(numList[1])
        zCoord = Decimal(numList[2])

        sfZCoord = zCoord * Decimal(scaleFactor)
        #spCoordFile = open (outCoordFile, 'a')
        intCoordFile.write (str(xCoord.quantize(Decimal('0.000001'), rounding = ROUND_UP)) + "   ")
        intCoordFile.write (str(yCoord.quantize(Decimal('0.000001'), rounding = ROUND_UP)) + "   ")
        intCoordFile.write (str(sfZCoord.quantize(Decimal('0.000001'), rounding = ROUND_UP))+"\n")

    intCoordFile.close()
    print "Success"


os.chdir("C:/Users/kevin.takala/Desktop")
coordFile = open(raw_input("Enter the coordinate file: "), 'r')
outCoordFile = raw_input ("Enter the output coordinate file: ")
ConvToSF()





