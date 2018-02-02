'''
Created on Feb 2, 2018

@author: Azhar
'''
scoreLine = "INFO: ps_lattice.c(1380): Bestpath score:"
hypoLine = "INFO: batch.c(763):"  # At scoreLine+7 or before ('done')

BaseDir = "/Users/Azhar/Desktop/MDC_Experiments/PDAmDigits/Results/"
model = 10
currentModel = "PDAmDigits" + str(model) + "dB.ci_cont"

inputSNR = 30   # Here to loop Model10: 30-50
                #              Model15: 40-50
logFile = "Digits"+str(inputSNR)+"On"+str(model)+ "-1-1.log"
fname = BaseDir + logFile

out_File = BaseDir + "Noisy_" + str(inputSNR) +"db/" + currentModel
print("Getting results of input "+ str(inputSNR) + " on mode "+ str(model) +" from " + fname)
print ("Storing result in: " + out_File)
ListOfFinalResults = []
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
            
           # print("Name: "+fNameOnly+ "   Hyp:" + hyp+ "   Score:"+ score+"   Confidence:"+ confidence)
            FinalResult = {"Name":fNameOnly, "Hyp": hyp, "Score": score, "Confidence": confidence}
            ListOfFinalResults.append(FinalResult)
        prev_line = line
        
