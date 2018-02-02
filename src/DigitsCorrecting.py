'''
Created on Feb 2, 2018

@author: Azhar
'''
import StoreResults as dump
import subprocess

scoreLine = "INFO: ps_lattice.c(1380): Bestpath score:"
hypoLine = "INFO: batch.c(763):"  # At scoreLine+7 or before ('done')

BaseDir = "/Users/Azhar/Desktop/MDC_Experiments/PDAmDigits/"
model = 10
currentModel = "PDAmDigits" + str(model) + "dB.ci_cont"

inputSNR = 30   # Here to loop Model10: 30-50
                #              Model15: 40-50
                
for inputSNR in range(40,55,5):
    
    logFile = "Digits"+str(inputSNR)+"On"+str(model)+ "-1-1.log"
    fname = BaseDir + "Results/"+ logFile
    outDir = BaseDir + "Results/Noisy_" + str(inputSNR) +"db/"
    out_File = outDir + currentModel
    
    print("Getting results of input "+ str(inputSNR) + " on mode "+ str(model) +" from " + fname)
    
    ListOfFinalResults = []
    HypText = []
    with open(fname) as fp:
        prev_line = "kkkk"
        for line in fp:  
            if line.find(scoreLine)> -1:
                #print line
                score = line.split(':',3)[3]
            if line.find("done")> -1:
                hyp0 = prev_line
                splitted = hyp0.split('(')
                hyp = splitted[0]
                fNameOnly = splitted[1].split(')',2)[0].split()[0]
                confidence = splitted[1].split(')',2)[0].split()[1]
                
                # Extract UttId from fNameOnly to be written in Hyp file
                UttId = fNameOnly
                UttId = UttId[::-1].replace("/", "-", 1)[::-1]
                UttId = UttId.split('/', 2)[-1]
                #print ("File: "+ fNameOnly) 
                #print fNameOnly
                HypText.append(hyp + " (" + UttId + ")\n") 
                
               # print("Name: "+fNameOnly+ "   Hyp:" + hyp+ "   Score:"+ score+"   Confidence:"+ confidence)
                FinalResult = {"Name":fNameOnly, "Hyp": hyp, "Score": score, "Confidence": confidence}
                ListOfFinalResults.append(FinalResult)
            prev_line = line
            
    
    
    print ("Storing result in: " + out_File)
    dump.TextWrite(HypText, outDir+currentModel+".txt")
    dump.CSVDictWrite(ListOfFinalResults, outDir+currentModel+"/All_"+currentModel+".csv")
    hypFile = outDir+currentModel+".txt" 
    RefFile = BaseDir+"Reference.txt"
    out_File = outDir+"WERReslts_"+currentModel+".txt"
    print 'Finish, now Calculating Error Rate, please wait \n'
    perl_script = subprocess.Popen(["perl", "./word_align.pl",'-silent',hypFile, RefFile, out_File])
    perl_script.wait()
    print '\n'