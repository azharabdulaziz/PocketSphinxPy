#!/usr/bin/python
import sys
import subprocess
import os
import errno
from subprocess import Popen, PIPE
import Error_calc
import my_Error_calc
import StoreResults as dump
from os import environ, path
from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *



# Define parameters
ExpName = "an4"    
#SNR_Level = "White50db"

BaseDir = "/Users/Azhar/Desktop/MDC_Experiments/" + ExpName + "/"
TestFileIds = BaseDir + "an4_test.fileids"
BaseWavPath = "/Users/Azhar/Desktop/Exp2/an4/"
ModelsPath = BaseDir + "an4/AN4_AM/";
AcModel0 ="an4_Clean.cd_cont_200";
AcModel20 ="an4_White20dB.cd_cont_200";
AcModel15 ="an4_White15dB.cd_cont_200";
AcModel10 ="an4_White10dB.cd_cont_200";
AcModel = [AcModel0, AcModel20,AcModel15,AcModel10]
TotalNoOfFiles = 130
LM = BaseDir + "an4.lm"
Dic = BaseDir + "an4.dic"

# Create a decoder with certain model
currentModel = AcModel[0]
AM = BaseDir+"AN4_AM/"+currentModel
print "Acoustic Model: " + AM
print "Language Model: " + LM
print "Dictionary: " + Dic

config = Decoder.default_config()
config.set_string('-logfn', '/dev/null')
config.set_string('-hmm', path.join(AM))
config.set_string('-lm', path.join(LM))
config.set_string('-dict', path.join(Dic))
decoder = Decoder(config)

# Start reading Test list
print "Decoding Test Audio Files"
#SNR_Level = ["wav", "wavWhite5db",]
for snr in range(0,55,5):
    if snr==0:
        ExpWavPath = BaseWavPath + "wav/"
        outDir = "Results/Clean/" + currentModel + "/"
        wavext = ".sph"
    else:
        ExpWavPath = BaseWavPath + "wavWhite"+str(snr)+"db/"
        outDir = "Results/Noisy_"+ str(snr)+"db/" +currentModel+"/"
        wavext = ".wav"
    print ExpWavPath
    # Check for exist outdir
    print "Output Dir: " +outDir
    
    if not os.path.exists(os.path.dirname(outDir)):
        try:
            os.makedirs(os.path.dirname(outDir))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
            
    outLattice = outDir+"Lattice/"
    if not os.path.exists(os.path.dirname(outLattice)):
        try:
            os.makedirs(os.path.dirname(outLattice))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise            
    outHypo = outDir+"Hypothesis/"
    if not os.path.exists(os.path.dirname(outHypo)):
        try:
            os.makedirs(os.path.dirname(outHypo))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise            

    outWerRes = outDir+"WER_Results/"
    if not os.path.exists(os.path.dirname(outWerRes)):
        try:
            os.makedirs(os.path.dirname(outWerRes))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise            
    # Start reading Test list
    print "Decoding Test Audio Files for "+ExpWavPath
    i=0
    with open(TestFileIds) as fp:
        FinalResult = {}
        ListOfFinalResults = []
        HypText = []
        for AudioFile_rp in fp:
            decoder.start_utt()
            xx = AudioFile_rp.strip('\n')
            fNameOnly=xx[::-1].replace("/","-",1)[::-1]
            fNameOnly = fNameOnly.split('/',1)[-1]
            AudioFile = ExpWavPath + xx + wavext
            #print ("Decoding File: " +AudioFile)
            #print "File Name Only: " + fNameOnly
            stream = open(AudioFile, 'rb')
            while True:
                buf = stream.read(1024)
                if buf:
                    decoder.process_raw(buf, False, False)
                else:
                    break
            decoder.end_utt()
            hypothesis = decoder.hyp()
            HypText.append(hypothesis.hypstr + " (" + fNameOnly + ")\n") 
            FinalResult = {"Name":fNameOnly, "Hyp": hypothesis.hypstr, "Score": hypothesis.best_score, "Confidence": hypothesis.prob}
            ListOfFinalResults.append(FinalResult)
            #print 'Best hypothesis: ', hypothesis.hypstr, " model score: ", hypothesis.best_score, " confidence: ", hypothesis.prob
            decoder.get_lattice().write(outLattice+fNameOnly +'.lat')
            decoder.get_lattice().write_htk(outLattice+fNameOnly +'.htk')
            i=i+1
            completed = (i/TotalNoOfFiles)
            s = "Processing " + str(completed) + " %"
            sys.stdout.write("*")
    # Running perl WER test
    print "\n"
    dump.TextWrite(HypText, outHypo+currentModel+".txt")
    dump.CSVDictWrite(ListOfFinalResults, outDir+"/All_"+currentModel+".csv")
    hypFile = outHypo+currentModel+".txt" 
    RefFile = BaseDir+"RefClean.txt"
    out_File = outWerRes+currentModel+".txt"
    perl_script = subprocess.Popen(["perl", "./word_align.pl",hypFile, RefFile, out_File])
    perl_script.wait()
    #print perl_script.poll()
         
            

# p = Popen(['./word_align.pl'], stdin=PIPE, stdout=PIPE)
# p.stdin.write(params)
# p.stdin.close()
# the_output = p.stdout.read()
#Error_calc.CalculateWER(hypFile, RefFile)
#my_Error_calc.CalcWER(hypFile, RefFile)

