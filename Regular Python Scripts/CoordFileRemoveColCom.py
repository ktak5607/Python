import os
import re
from decimal import*


def RemoveCol():
    spCoordFile = open (outCoordFile, 'w')
    if (fileType == "space"):
        for line in coordFile:
            numList = line.split()
            del numList[cols-1]
            if (form == "NaNEZ"):
                
                name = numList[0]
                xCoord = Decimal(numList[1])
                yCoord = Decimal(numList[2])
                zCoord = Decimal(numList[3])
                
                if (len(name) <= 9):
                  spCoordFile.write (name + "    ")
                  spCoordFile.write (str(xCoord) + "   ")
                  spCoordFile.write (str(yCoord) + "   ")
                  spCoordFile.write (str(zCoord)+"\n")
                        
                elif (len(name) > 9):
                    spCoordFile.write (name + "   ")
                    spCoordFile.write (str(xCoord) + "   ")
                    spCoordFile.write (str(yCoord) + "   ")
                    spCoordFile.write (str(zCoord) + "\n")
                    
            elif (form == "NEZ"):
                
                xCoord = Decimal(numList[0])
                yCoord = Decimal(numList[1])
                zCoord = Decimal(numList[2])
                spCoordFile.write (str(xCoord) + "   ")
                spCoordFile.write (str(yCoord) + "   ")
                spCoordFile.write (str(zCoord) + "\n")
                
    elif (fileType == "comma"):
        for line in coordFile:
            numList = line.split(",")
            del numList[cols-1]
            if (form == "NaNEZ"):
                name = numList[0]
                xCoord = Decimal(numList[1])
                yCoord = Decimal(numList[2])
                zCoord = Decimal(numList[3])
                
                if (len(name) <= 9):
                  spCoordFile.write (name + "    ")
                  spCoordFile.write (str(xCoord) + "   ")
                  spCoordFile.write (str(yCoord) + "   ")
                  spCoordFile.write (str(zCoord)+"\n")
                        
                elif (len(name) > 9):
                    spCoordFile.write (name + "   ")
                    spCoordFile.write (str(xCoord) + "   ")
                    spCoordFile.write (str(yCoord) + "   ")
                    spCoordFile.write (str(zCoord) + "\n")
                    
            elif (form == "NEZ"):
                
                xCoord = Decimal(numList[0])
                yCoord = Decimal(numList[1])
                zCoord = Decimal(numList[2])
                spCoordFile.write (str(xCoord) + "   ")
                spCoordFile.write (str(yCoord) + "   ")
                spCoordFile.write (str(zCoord) + "\n")
    spCoordFile.close()    
    print "Success"



def RemoveCommas():
    spCoordFile = open (outCoordFile, 'w')
    for line in coordFile:
            numList = line.split(",")
            if(form == "NaNEZ"):
                name = numList[0]
                xCoord = Decimal(numList[1])
                yCoord = Decimal(numList[2])
                zCoord = Decimal(numList[3])
                
                if (len(name) <= 9):
                  spCoordFile.write (name + "   ")
                  spCoordFile.write (str(xCoord) + "   ")
                  spCoordFile.write (str(yCoord) + "   ")
                  spCoordFile.write (str(zCoord)+"\n")
                        
                if (len(name) > 9):
                    spCoordFile.write (name + "   ")
                    spCoordFile.write (str(xCoord) + "   ")
                    spCoordFile.write (str(yCoord) + "   ")
                    spCoordFile.write (str(zCoord) + "\n")
                    
            elif (form == "NEZ"):
                
                xCoord = Decimal(numList[0])
                yCoord = Decimal(numList[1])
                zCoord = Decimal(numList[2])
                spCoordFile.write (str(xCoord) + "   ")
                spCoordFile.write (str(yCoord) + "   ")
                spCoordFile.write (str(zCoord) + "\n")
                    
    spCoordFile.close()    
    print "Success"
    
os.chdir("C:/Users/kevin.takala/Desktop")
coordFile = open(raw_input("Enter the coordinate file: "), 'r')
editType = raw_input("Enter what you want to edit (remove columns(rcol), Remove Commas(rcom)): ")
cols = 0
form = raw_input("Enter output format of the file (NaNEZ or NEZ): ")
if editType == "rcol":
    cols = int(raw_input("Enter the column to remove: "))
#coordOrder = raw_input("Please enter the order that the coordinates appear (NaNEZ,NaENZ). ") 
fileType = str(raw_input("Enter the delimeter between columns. (comma or space): "))
outCoordFile = raw_input ("Enter the output coordinate file: ")
if editType == "rcol":
    RemoveCol()
elif editType == "rcom":
    RemoveCommas()
else:
    print "You entered an invalid coordinate system to convert to. Try again later."
    


