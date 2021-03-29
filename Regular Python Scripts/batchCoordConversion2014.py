import os
import re
from decimal import*

#Convert to State Plane Coordinates
def ConvToSP():
    spCoordFile = open (outCoordFile, 'a')
    if (fileType == "space"):
        for line in coordFile:
            numList = re.sub(" ", " ", line).split()
            name = numList[0]
            xCoord = Decimal(numList[1])
            yCoord = Decimal(numList[2])
            zCoord = Decimal(numList[3])
            
            spXCoord = xCoord/scaleFactor
            spYCoord = yCoord/scaleFactor
            spCoordFile = open (outCoordFile, 'a')
                
            if (len(name) <= 9):
              spCoordFile.write (name + "    ")
            spCoordFile.write (str(spXCoord.quantize(Decimal('0.0001'), rounding = ROUND_UP)) + "   ")
            spCoordFile.write (str(spYCoord.quantize(Decimal('0.0001'), rounding = ROUND_UP)) + "   ")
            spCoordFile.write (str(zCoord)+"\n")
                    
            if (len(name) > 9):
                spCoordFile.write (name + "   ")
                spCoordFile.write (str(spXCoord.quantize(Decimal('0.0001'), rounding = ROUND_UP)) + "   ")
                spCoordFile.write (str(spYCoord.quantize(Decimal('0.0001'), rounding = ROUND_UP)) + "   ")
                spCoordFile.write (str(zCoord) + "\n")
                    
                
    elif (fileType == "comma"):
        for line in coordFile:
            numList = re.sub(",", " ", line).split()
            name = numList[0]
            xCoord = Decimal(numList[1])
            yCoord = Decimal(numList[2])
            zCoord = Decimal(numList[3])
            
            spXCoord = xCoord/scaleFactor
            spYCoord = yCoord/scaleFactor
            
                
            if (len(name) <= 9):
              spCoordFile.write (name + "    ")
              spCoordFile.write (str(spXCoord.quantize(Decimal('0.0001'), rounding = ROUND_UP)) + "   ")
              spCoordFile.write (str(spYCoord.quantize(Decimal('0.0001'), rounding = ROUND_UP)) + "   ")
              spCoordFile.write (str(zCoord)+"\n")
                    
            if (len(name) > 9):
                spCoordFile.write (name + "   ")
                spCoordFile.write (str(spXCoord.quantize(Decimal('0.0001'), rounding = ROUND_UP)) + "   ")
                spCoordFile.write (str(spYCoord.quantize(Decimal('0.0001'), rounding = ROUND_UP)) + "   ")
                spCoordFile.write (str(zCoord) + "\n")
    spCoordFile.close()    
    print "Success"



def ConvToV14():
    spCoordFile = open (outCoordFile, 'a')
    if (fileType == "space"):
        for line in coordFile:
            numList = re.sub(" ", " ", line).split()
            name = numList[0]
            xCoord = Decimal(numList[1])
            yCoord = Decimal(numList[2])
            zCoord = Decimal(numList[3])
            
            spXCoord = xCoord * scaleFactor
            spYCoord = yCoord * scaleFactor
            spCoordFile = open (outCoordFile, 'a')
                
            if (len(name) <= 9):
              spCoordFile.write (name + "    ")
              spCoordFile.write (str(spXCoord.quantize(Decimal('0.0001'), rounding = ROUND_UP)) + "   ")
              spCoordFile.write (str(spYCoord.quantize(Decimal('0.0001'), rounding = ROUND_UP)) + "   ")
              spCoordFile.write (str(zCoord)+"\n")
                    
            if (len(name) > 9):
                spCoordFile.write (name + "   ")
                spCoordFile.write (str(spXCoord.quantize(Decimal('0.0001'), rounding = ROUND_UP)) + "   ")
                spCoordFile.write (str(spYCoord.quantize(Decimal('0.0001'), rounding = ROUND_UP)) + "   ")
                spCoordFile.write (str(zCoord) + "\n")
                    
                
    elif (fileType == "comma"):
        for line in coordFile:
            numList = re.sub(",", " ", line).split()
            name = numList[0]
            xCoord = Decimal(numList[1])
            yCoord = Decimal(numList[2])
            zCoord = Decimal(numList[3])
            
            spXCoord = xCoord * scaleFactor
            spYCoord = yCoord * scaleFactor
            
                
            if (len(name) <= 9):
              spCoordFile.write (name + "    ")
              spCoordFile.write (str(spXCoord.quantize(Decimal('0.0001'), rounding = ROUND_UP)) + "   ")
              spCoordFile.write (str(spYCoord.quantize(Decimal('0.0001'), rounding = ROUND_UP)) + "   ")
              spCoordFile.write (str(zCoord)+"\n")
                    
            if (len(name) > 9):
                spCoordFile.write (name + "   ")
                spCoordFile.write (str(spXCoord.quantize(Decimal('0.0001'), rounding = ROUND_UP)) + "   ")
                spCoordFile.write (str(spYCoord.quantize(Decimal('0.0001'), rounding = ROUND_UP)) + "   ")
                spCoordFile.write (str(zCoord) + "\n")
    spCoordFile.close()    
    print "Success"
    
os.chdir("C:/Users/kevin.takala/Desktop")
convTo = str(raw_input("Enter the coordinate system you want to convert to. (SP or V14): "))
coordFile = open(raw_input("Enter the coordinate file: "), 'r')
scaleFactor = Decimal(raw_input("Enter the scale factor for the area: "))
#filefrmt + raw_input("Enter the coordinate format of the file (NaNEZ, NaENZ, 
coordOrder = raw_input("Please enter the order that the coordinates appear (NaNEZ,NaENZ). ") 
fileType = str(raw_input("Enter the delimeter between columns. (comma or space): "))
outCoordFile = raw_input ("Enter the output coordinate file: ")
if (convTo == "SP"):
    ConvToSP()
elif (convTo == "V14"):
    ConvToV14()
else:
    print "You entered an invalid coordinate system to convert to. Try again later."
    


