import os
import re
from decimal import*

#Convert to State Plane Coordinates
def ConvToInt():
    intCoordFile = open (outCoordFile, 'a')

    for line in coordFile:
        numList = re.sub(" ", " ", line).split()
        scaleFactor = 0.999998000004
        name = numList[0]
        xCoord = Decimal(numList[1])
        yCoord = Decimal(numList[2])
        zCoord = Decimal(numList[3])

        intXCoord = xCoord / Decimal(scaleFactor)
        intYCoord = yCoord / Decimal(scaleFactor)
        intZCoord = zCoord / Decimal(scaleFactor)
        #spCoordFile = open (outCoordFile, 'a')
        intCoordFile.write (name + "   ")
        intCoordFile.write (str(intXCoord.quantize(Decimal('0.000001'), rounding = ROUND_UP)) + "   ")
        intCoordFile.write (str(intYCoord.quantize(Decimal('0.000001'), rounding = ROUND_UP)) + "   ")
        intCoordFile.write (str(intZCoord.quantize(Decimal('0.000001'), rounding = ROUND_UP))+"\n")

    intCoordFile.close()
    print "Success"



def ConvToSurv():
    survCoordFile = open (outCoordFile, 'a')
    for line in coordFile:
        numList = re.sub(" ", " ", line).split()
        scaleFactor = 0.999998000004
        name = numList[0]
        xCoord = Decimal(numList[1])
        yCoord = Decimal(numList[2])
        zCoord = Decimal(numList[3])

        survXCoord = xCoord * Decimal(scaleFactor)
        survYCoord = yCoord * Decimal(scaleFactor)
        survZCoord = zCoord * Decimal(scaleFactor)
        #spCoordFile = open (outCoordFile, 'a')
        survCoordFile.write (name + "   ")
        survCoordFile.write (str(survXCoord.quantize(Decimal('0.000001'), rounding = ROUND_UP)) + "   ")
        survCoordFile.write (str(survYCoord.quantize(Decimal('0.000001'), rounding = ROUND_UP)) + "   ")
        survCoordFile.write (str(survZCoord.quantize(Decimal('0.000001'), rounding = ROUND_UP))+"\n")

    survCoordFile.close()
    print "Success"

os.chdir("C:/Users/kevin.takala/Desktop")
convTo = str(raw_input("Enter the coordinate system you want to convert to. (surv or int): "))
coordFile = open(raw_input("Enter the coordinate file: "), 'r')
outCoordFile = raw_input ("Enter the output coordinate file: ")
if (convTo == "surv"):
    ConvToSurv()
elif (convTo == "int"):
    ConvToInt()
else:
    print "You entered something incorrectly, please try again."




