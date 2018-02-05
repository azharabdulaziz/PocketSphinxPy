'''
Created on Feb 4, 2018

@author: Azhar
'''
'''
Created on Feb 2, 2018

@author: Azhar
'''

import os
import errno
import StoreResults as dump
import subprocess
import csv

scoreLine = "INFO: ps_lattice.c(1380): Bestpath score:"
hypoLine = "INFO: batch.c(762):"  # At scoreLine+7 or before ('done')

BaselogDir = "/Users/Azhar/Desktop/Exp1/timit/logdir/decode/"
BaseDir = "/Users/Azhar/Desktop/MDC_Experiments/TIMIT/"
#model = 10 # Variable
#logFile = "crossCrowd_5on5-1-1"


#model = 10 # Variable
for model_ind in range(3,4):
    if model_ind == 0:
        model = 10
    elif model_ind == 1:
        model = 15
    elif model_ind == 2:
        model = 20
    elif model_ind == 3:
        model ='Clean'
    
    for inputSNR in range(5,55,5):
        BaseOutDir = BaseDir + "BabbleResults/Noisy_" + str(inputSNR) +"db/"
        # Check for exist outdir
        if not os.path.exists(os.path.dirname(BaseOutDir)):
            try:
                os.makedirs(os.path.dirname(BaseOutDir))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
    
        '''
        # Reading STS-SNR
        LLS_CsvFile = BaseDir+"LLsResults/"+ "MDL_LLs"+ str(inputSNR) +"dB.csv"
        print("Reading STS-SNR logProb from: "+ LLS_CsvFile)
        with open(LLS_CsvFile, 'r') as AllLogProb:
            snrLogProb = csv.reader(AllLogProb)
            logProb = list(snrLogProb)
        
        ModelID = 0 # 0: AM10  1:AM15  2:AM20   3:AM_clean
        fileNo = 0
        
        print("LogProb: " + str(logProb[fileNo]))
        
        x = []
        for i in range(0,4):
            x.append(float( logProb[fileNo][i]))
        model_ind = x.index(max(x))
        if model_ind == 0:
            model = 10
        elif model_ind == 1:
            model = 15
        elif model_ind == 2:
            model = 20
        elif model == 3:
            model ='Clean'
        
        
        '''
        print ("Input SNR = " + str(inputSNR))
        print("Model ind = " + str(model))
        
        if (inputSNR == model):
            logFile = "timit_Crowd"+str(inputSNR)+ "dB-1-1.log"
        else :
            logFile = "crossCrowd_"+str(inputSNR)+"on"+str(model)+ "-1-1.log"
        
        if model == 'Clean':
            logFile = "crossCrowd"+str(inputSNR)+"on"+str(model)+ "-1-1.log"
            currentModel = "TIMIT_" + str(model) + ".cd_cont_200"
        else:
            currentModel = "TIMIT_" + str(model) + "dB.cd_cont_200"
        
        fname = BaselogDir + logFile
        
    
        
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
                
        
       
        
        OutDir = BaseOutDir + currentModel +"/"     
        # Check for exist outdir
        if not os.path.exists(os.path.dirname(OutDir)):
            try:
                os.makedirs(os.path.dirname(OutDir))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        print ("Storing result in: " +OutDir)
        dump.TextWrite(HypText, currentModel+".txt")
        dump.CSVDictWrite(ListOfFinalResults, OutDir+"All_"+currentModel+".csv")
        '''
        hypFile = currentModel+".txt" 
        RefFile = BaseDir+"RefClean.txt"
        out_File = BaseOutDir+"WERReslts_"+currentModel+".txt"
        print 'Finish, now Calculating Error Rate, please wait \n'
        perl_script = subprocess.Popen(["perl", "./word_align.pl",'-silent',hypFile, RefFile, out_File])
        perl_script.wait()
        print '\n'
        '''