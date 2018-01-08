#!/usr/bin/python2.7
import StoreResults as dump
ExpName = "WSJ"    
#SNR_Level = "White50db"
TotalNoOfFiles = 35
BaseDir = "/Users/Azhar/Desktop/MDC_Experiments/" + ExpName + "/"
inputFile = BaseDir + "Clean-1-1.log" 
outFile = BaseDir + "Reference.txt"
outString = []
with open(inputFile,'r') as inFile, open(outFile,'w') as out:
    lines = inFile.readlines()
    flag = False
    for line in lines:
        if(flag):
            uttID = line.split('/',1)[-1]
            uttID = "(" + uttID.split(' ',1)[0] + ")"
            uttID = uttID.replace('/','-')
            uttID = uttID.replace('_1','_5')
            line = line.split('(',1)[0] + uttID +'\n'
            outString.append(line)
            flag = False
        
        if(line.find('INFO: batch.c(762):') != -1):
            flag = True
    
    print outString
    dump.TextWrite(outString, outFile)
    