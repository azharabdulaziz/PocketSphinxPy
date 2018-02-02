'''
Created on Feb 1, 2018

@author: Azhar
'''
'''
Created on Feb 1, 2018

@author: Azhar
'''
#!/usr/bin/python2.7
"""
Introduction
This function reads the decoder results csv file in MDC_Experiment directory. 
Then,for each $TestFile it compares the score of the four modules.
This approach is Multiple decoder voting MDV based on Score only

/**
     * The STSlogProb comes from LLsResults folder, which is formed by LLSExtractor.
     * <p>
     * LLsExtractor : 
     * <p>
     * Takes the trained parameters table values from audio of different noise levels and estimates the 
     * LogLiklihood of each file in the test part. It stores  MDL_LLsxdB.csv table, where x=5:5:50 dB SNR 
     * in the folder ~/LLsResults/.
     * <p>
     * Those files has the following arrangement:
     * <p>
     * 
     *                 S_1    S_2    S_3    S_4
     * <p>
     * <p>
     *         file_1
     * <p>
     *         file_2
     * <p>
     *         .
     * <p>
     *         .
     * <p>
     *         .
     * <p>
     *         last file in test
     * <p>
     * Where S_i = {<10, 15 ,20 , Clean or >20} AM. 
     * 
     * 
     * @param csvFile: the absolute path of the MDL_LLsxdB.csv file
     * @return 
     * @author Azhar Sabah Abdulaziz
     */
    



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
        #print("Reading Result file: "+ CSVfileName)
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
    
    LLS_CsvFile = BaseDir+"LLsResults/"+ "LMDL_LLs"+ str(snr_level) +"dB.csv"
    print("Reading STS-SNR logProb from: "+ LLS_CsvFile)
    with open(LLS_CsvFile, 'r') as AllLogProb:
        snrLogProb = csv.reader(AllLogProb)
        logProb = list(snrLogProb)
        
        
    TotalNoOfFiles = len(ResultClean)-1
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
        
        ScoreList.append(ResultClean[i][score_ind]+ logProb[i][3]) # if bestScoreInd = 0
        #print("LogProb["+str(i)+"]: "+ logProb[i][3])
        ScoreList.append(Result10[i][score_ind]+ logProb[i][0])    # if bestScoreInd = 1
        ScoreList.append(Result15[i][score_ind]+ logProb[i][1])    # if bestScoreInd = 2
        ScoreList.append(Result20[i][score_ind]+ logProb[i][2])    # if bestScoreInd = 3
        bestScoreInd = ScoreList.index(min(ScoreList))
        
        # Best Hypothesis
        
        if(ExpName == 'timit'):
            UttId = ResultClean[i][fName_ind]
            UttId = UttId[::-1].replace("/", "-", 1)[::-1]
            UttId = UttId.split('/', 2)[-1]
        else:
            UttId = ResultClean[i][fName_ind]
        #print("UttID: " + UttId)  
        BestHypo.append(hypList[bestScoreInd]+' ('+UttId + ')\n')
    
    
    #print best_utt
    MDC_Hyp = outDir+"MDVAlphaAligne_Score.txt"
    print("\n Writing MDV results in " + MDC_Hyp)
    dump.TextWrite(BestHypo, MDC_Hyp)
    
    print 'Finish, now Calculating Error Rate, please wait \n'
    RefFile = BaseDir+"RefClean.txt"
    out_File = outDir+"MDV_ScoreWithAlpha_WERReslts.txt"
    perl_script = subprocess.Popen(["perl", "./word_align.pl",'-silent',MDC_Hyp, RefFile, out_File])
    perl_script.wait()
