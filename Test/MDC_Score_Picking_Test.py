#!/usr/bin/python2.7
"""
Introduction
This function reads the decoder results csv file in MDC_Experiment directory. Then,for each $TestFile it compares the score of the four modules.
This approach is Multiple decoder voting based on Score   
"""

import csv
import StoreResults as dump
import subprocess


ExpName = 'an4'
whichScore = 'c'
if(ExpName == 'an4'):
    an4_addition = '_White'
else:
    an4_addition ='_'
BaseDir = "/Users/Azhar/Desktop/MDC_Experiments/" + ExpName + "/"
AcModel0 =ExpName+"_Clean.cd_cont_200";
AcModel20 =ExpName+an4_addition+"20dB.cd_cont_200";
AcModel15 =ExpName+an4_addition+"15dB.cd_cont_200";
AcModel10 =ExpName+an4_addition+"10dB.cd_cont_200";
AcModel = [AcModel0, AcModel10, AcModel15, AcModel20]
Hyp=[]
Conf = []
Score = []
TestFile = []
#snr_level =0
for snr_level in range(0,55,5):
    if(snr_level == 0):
        snr = 'Clean/'
    else:
        snr = "Noisy_"+str(snr_level)+"db/"
        
    outDir = BaseDir+"Results/"+snr
    
    CSVfileName = []
    for current_model in range(0,4):
        #print ("Calculating for AM: " + AcModel[current_model])
        inDir = BaseDir+"Results/"+ snr + AcModel[current_model] + "/"
        CSVfileName.append(inDir+"All_"+AcModel[current_model]+".csv")
        #print("Reading file: "+ CSVfileName)
    with open(CSVfileName[0], 'r') as AM_Clean, open(CSVfileName[1],'r') as AM_10, open(CSVfileName[2],'r') as AM_15, open(CSVfileName[3],'r') as AM_20:
        
        H=[]
        C = []
        S = []
        T = []
        CleanReader = csv.reader(AM_Clean)
        AM10Reader = csv.reader(AM_10)
        AM15Reader = csv.reader(AM_15)
        AM20Reader = csv.reader(AM_20)
        ResultClean = list(CleanReader)
        Result10 = list(AM10Reader)
        Result15 = list(AM15Reader)
        Result20 = list(AM20Reader)
    # Close all opened CSV files
    
    TotalNoOfFiles = len(ResultClean)
    print('TotalNoOfFiles = ' + str(TotalNoOfFiles))
    # For each utterance, starting from 1 to skip CSV headers
    Headers = ResultClean[0]
    print('Headers: ' + str(Headers))
    conf_ind = 1
    score_ind= 2
    fName_ind = 3
    hyp_ind = 0
    BestHypo = []
    for i in range(1,TotalNoOfFiles):
        ScoreList = []
        hypList = []
        hypList.append(ResultClean[i][hyp_ind])
        hypList.append(Result10[i][hyp_ind])
        hypList.append(Result15[i][hyp_ind])
        hypList.append(Result20[i][hyp_ind])
        if(whichScore == 's'):
            ind = score_ind
        if(whichScore == 'c'):
            ind = conf_ind
        
        ScoreList.append(ResultClean[i][ind]) # if bestScoreInd = 0
        ScoreList.append(Result10[i][ind])    # if bestScoreInd = 1
        ScoreList.append(Result15[i][ind])    # if bestScoreInd = 2
        ScoreList.append(Result20[i][ind])    # if bestScoreInd = 3
        bestScoreInd = ScoreList.index(max(ScoreList))
        
        # Best Hypothesis
        
        if(ExpName == 'TIMIT'):
            UttId = ResultClean[i][fName_ind]
            UttId = UttId[::-1].replace("/", "-", 1)[::-1]
            UttId = UttId.split('/', 2)[-1]
        else:
            UttId = ResultClean[i][fName_ind]
            
        BestHypo.append(hypList[bestScoreInd]+' ('+UttId + ')\n')
    
    
    #print best_utt
    MDC_Hyp = outDir+"MDC_Result.txt"
    print("\n Writing MDC results in " + MDC_Hyp)
    dump.TextWrite(BestHypo, MDC_Hyp)
    
    print 'Finish, now Calculating Error Rate, please wait \n'
    print('Input: ' + snr)
    RefFile = BaseDir+"RefClean.txt"
    out_File = outDir+"Clean_MDC_WERReslts.txt"
    perl_script = subprocess.Popen(["perl", "./word_align.pl",'-silent',MDC_Hyp, RefFile, out_File])
    perl_script.wait()
