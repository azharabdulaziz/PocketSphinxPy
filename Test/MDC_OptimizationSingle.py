#!/usr/bin/python2.7
"""
Introduction
This function reads the decoder results csv file in MDC_Experiment directory. Then,for each $TestFile it compares the score of the four modules.  
"""
import sys
import csv
import StoreResults as dump
import subprocess
from source import Error_calc
import matplotlib.pyplot as graph


ExpName = 'an4'
whichScore = 0
uttind = 4
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
snr_level =0
#for snr_level in range(0,55,5):
if(snr_level == 0):
    snr = 'Clean/'
else:
    snr = "Noisy_"+str(snr_level)+"db/"
    
outDir = BaseDir+"Results/"+snr

for current_model in range(0,4):
    print ("Calculating for AM: " + AcModel[current_model])
    inDir = BaseDir+"Results/"+ snr + AcModel[current_model] + "/"
    CSVfileName = inDir+"All_"+AcModel[current_model]+".csv"
    #print("Reading file: "+ CSVfileName)
    with open(CSVfileName, 'r') as myfile:
        H=[]
        C = []
        S = []
        T = []
        reader = csv.reader(myfile)
        c = 0
        for element in reader:
            # to skip the header row
            c = c+1
            if(c == 1):
                continue
            if(c ==3 ):
                break
            H.append(element[0])
            C.append(element[1])
            S.append(element[2])
            T.append(element[3]) 
    Hyp.append(H)
    Conf.append(C)
    Score.append(S)
    TestFile.append(T) 
    
#     print ("For AM: " + AcModel[current_model] + " Hyp is: " + Hyp[current_model][uttind]+ " Score=" 
#            + Score[current_model][uttind] + " Conf=" + Conf[current_model][uttind])

############# End of for loop
#print("Number of test utterances: " + str(counter))
"""
Now, find the highest score for each utterance.
"""
best_utt = []
B_model =[]
total_utt = len(Hyp[0])
print ("Number of of utt: "+str(total_utt))
for utt in range(0,total_utt):
    """
    OPTIMIZATION ~~~~~~~~~~~~~~~~~~~
    """
    WER = []
    for w0 in range(10,0,-1):
        b_model=[]
        score_test=[]
    
        w1 = 10-w0
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ O P T I M I Z A T I O N ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('                    w0 = ' + str(0.1*w0) + '                    w1 = ' + str(0.1*w1))
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        for model in range(0,4):
            score1 = int(Score[model][utt])
            score2 = int(Conf[model][utt])
            
            score = (w0*score1+w1*score2)/20
            print('Model: ' + AcModel[model] + '   Hyp: '+ Hyp[model][utt]+'(' +TestFile[model][utt]+')'+'   Score = ' + str(score))
    #         if(whichScore == 0):
    #             score = Score[model][utt]
    #             print('Score = ' + score)
    #         if(whichScore == 1):
    #             score = Conf[model][utt]
    #             print('Score = ' + score)
    #         else:
    #             sys.exit('Error: score option is not set, please use score or conf')
    #    
            score_test.append(score)
            # Python min and max works on absolute values, therefore; max score is min(socre_test)
            b_model.append(score_test.index(max(score_test)))
        B_model.append(b_model)
             
        # Find the best model that gives the maximum score_test  
        best_model = score_test.index(max(score_test))
        print('Score=')
        print score_test
        print('Max Score = ' + str(max(score_test)))
        print('Index of MAX score: ' + str(best_model))
    
        if(ExpName == 'TIMIT'):
            UttId = TestFile[best_model][utt]
            UttId = UttId[::-1].replace("/", "-", 1)[::-1]
            UttId = UttId.split('/', 2)[-1]
        else:
            UttId = TestFile[best_model][utt]
        best_utterance = Hyp[best_model][utt]+" (" + UttId + ")\n"
        print("Best Utterance: " + best_utterance)
        
        ## Error Rate Calculations
        RefFile = BaseDir+"RefClean.txt"
        with open(RefFile) as fp:
            ref = fp.readline()
            print('Reference: ' + ref)
        [Ins,Del,Sub,Correct,Sen_err,no_words] = Error_calc.sentence_error(best_utterance.upper(),ref.upper())
        N = Sub + Del + Correct
        ERR = Sub + Del + Ins
        WERP = 100*ERR/float(N)  
#         print('Ins=' +str(Ins) +' Del= '+  str(Del) + ' Sub = '+ str(Sub) + ' Correct = '+ str(Correct) +'  Total Words: ' + str(N))      
#         print('WER = ' + str(WERP)+'%')
        WER.append(WERP)
    """
    OPTIMIZATION ~~~~~~~~~~~~~~~~~~~
    """
w0 = range(10,0,-1)
w1 = range(0,10)
minWER = min(WER)
ind = WER.index(minWER)
print('WER' + str(WER))
print('WER_min = ' + str(minWER) + '  At w0 = ' + str(0.1*w0[ind])+ '    w1 = ' + str(0.1*w1[ind]))
