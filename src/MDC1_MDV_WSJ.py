'''
Created on Feb 2, 2018

@author: Azhar
'''
#!/usr/bin/python2.7
"""
Introduction
This function reads the decoder results csv file in MDC_Experiment directory. 
Then,for each $TestFile it compares the score of the four modules.
This approach is Multiple decoder voting MDV based on Score only
"""

import csv
import StoreResults as dump
import subprocess


ExpName = 'wsj'

BaseDir = "/Users/Azhar/Desktop/MDC_Experiments/" + ExpName + "/"
AcModel0 ="Clean.cd_cont_200";
AcModel20 ="White20dB.cd_cont_200";
AcModel15 ="White15dB.cd_cont_200";
AcModel10 ="White10dB.cd_cont_200";
AcModel = [AcModel0, AcModel10, AcModel15, AcModel20]
Hyp=[]
Conf = []
Score = []
TestFile = []

for snr_level in range(5,55,5):
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
        CleanReader = csv.reader(AM_Clean)
        AM10Reader = csv.reader(AM_10)
        AM15Reader = csv.reader(AM_15)
        AM20Reader = csv.reader(AM_20)
        
        next(CleanReader, None)  # skip the headers
        next(AM10Reader, None)  # skip the headers
        next(AM15Reader, None)  # skip the headers
        next(AM20Reader, None)  # skip the headers
        
        ResultClean = list(CleanReader)
        Result10 = list(AM10Reader)
        Result15 = list(AM15Reader)
        Result20 = list(AM20Reader)
    # Close all opened CSV files
    
    TotalNoOfFiles = len(ResultClean)
    print('TotalNoOfFiles = ' + str(TotalNoOfFiles))
    # For each utterance, starting from 1 to skip CSV headers
    
    score_ind= 2   # 1 Confidence   2 Score
    fName_ind = 3
    hyp_ind = 0
    BestHypo = []
    for i in range(0,TotalNoOfFiles):
        ScoreList = []
        hypList = []
        hypList.append(ResultClean[i][hyp_ind])
        hypList.append(Result10[i][hyp_ind])
        hypList.append(Result15[i][hyp_ind])
        hypList.append(Result20[i][hyp_ind])
        
        ScoreList.append(ResultClean[i][score_ind]) # if bestScoreInd = 0
        ScoreList.append(Result10[i][score_ind])    # if bestScoreInd = 1
        ScoreList.append(Result15[i][score_ind])    # if bestScoreInd = 2
        ScoreList.append(Result20[i][score_ind])    # if bestScoreInd = 3
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
    MDC_Hyp = outDir+"MDC_Result_Score.txt"
    print("\n Writing MDC results in " + MDC_Hyp)
    dump.TextWrite(BestHypo, MDC_Hyp)
    
    print 'Finish, now Calculating Error Rate, please wait \n'
    RefFile = BaseDir+"RefClean.txt"
    out_File = outDir+"Aligned_MDC_Score_WERReslts.txt"
    perl_script = subprocess.Popen(["perl", "./word_align.pl",'-silent',MDC_Hyp, RefFile, out_File])
    perl_script.wait()
