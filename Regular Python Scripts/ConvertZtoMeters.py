import os
import re
from decimal import*

#Convert heights to meters
def ConvToSF():
    sfCoordFile = open (outCoordFile, 'w')

    for line in coordFile:
        numList = re.sub(" ", " ", line).split()
        scaleFactor = 1/3.280833333333
        xCoord = Decimal(numList[0])
        yCoord = Decimal(numList[1])
        zCoord = Decimal(numList[2])

        mZCoord = zCoord * Decimal(scaleFactor)
        #spCoordFile = open (outCoordFile, 'a')
        sfCoordFile.write (str(xCoord.quantize(Decimal('0.000001'), rounding = ROUND_UP)) + "   ")
        sfCoordFile.write (str(yCoord.quantize(Decimal('0.000001'), rounding = ROUND_UP)) + "   ")
        sfCoordFile.write (str(mZCoord.quantize(Decimal('0.000001'), rounding = ROUND_UP))+"\n")

    intCoordFile.close()
    print "Success"


#os.chdir("C:/Users/kevin.takala/Desktop")
coordFile = open(r"C:/Users/kevin.takala/Desktop/111015_LiDAR.txt", 'r')
outCoordFile = r"C:/Users/kevin.takala/Desktop/111015_LiDAR_Meters.txt"
ConvToSF()





