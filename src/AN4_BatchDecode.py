#!/usr/bin/python2.7
import sys
import subprocess
import os
import errno
from subprocess import Popen
import StoreResults as dump
from os import path
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

LM = BaseDir + "an4.lm"
Dic = BaseDir + "an4.dic"

# Create a decoder with certain model
for currentModel in AcModel:
    AM = BaseDir + "AN4_AM/" + currentModel
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
    # SNR_Level = ["wav", "wavWhite5db",]
    for snr in range(0, 55, 5):
        if snr == 0:
            ExpWavPath = BaseWavPath + "wav/"
            outDir = BaseDir+"Results/Clean/" + currentModel + "/"
            wavext = ".sph"
        else:
            ExpWavPath = BaseWavPath + "wavWhite" + str(snr) + "db/"
            outDir = BaseDir+"Results/Noisy_" + str(snr) + "db/" + currentModel + "/"
            wavext = ".wav"
            
        # Check for exist outdir
        if not os.path.exists(os.path.dirname(outDir)):
            try:
                os.makedirs(os.path.dirname(outDir))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
                
        outLattice = outDir + "Lattice/"
        if not os.path.exists(os.path.dirname(outLattice)):
            try:
                os.makedirs(os.path.dirname(outLattice))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise            
        # Start reading Test list
        print "Decoding Test Audio Files for " + ExpWavPath + " using AM " + currentModel
        with open(TestFileIds) as fp:
            FinalResult = {}
            ListOfFinalResults = []
            HypText = []
            for AudioFile_rp in fp:
                decoder.start_utt()
                xx = AudioFile_rp.strip('\n')
                fNameOnly = xx[::-1].replace("/", "-", 1)[::-1]
                fNameOnly = fNameOnly.split('/', 1)[-1]
                AudioFile = ExpWavPath + xx + wavext
                # print ("Decoding File: " +AudioFile)
                # print "File Name Only: " + fNameOnly
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
                # print 'Best hypothesis: ', hypothesis.hypstr, " model score: ", hypothesis.best_score, " confidence: ", hypothesis.prob
                decoder.get_lattice().write(outLattice + fNameOnly + '.lat')
                decoder.get_lattice().write_htk(outLattice + fNameOnly + '.htk')
                sys.stdout.write("*")
        # Running perl WER test
        print "\n"
        
        dump.TextWrite(HypText, outDir+currentModel+".txt")
        dump.CSVDictWrite(ListOfFinalResults, outDir+"/All_"+currentModel+".csv")
        hypFile = outDir+currentModel+".txt" 
        RefFile = BaseDir+"RefClean.txt"
        out_File = outDir+"WERReslts_"+currentModel+".txt"
        perl_script = subprocess.Popen(["perl", "./word_align.pl",'-silent' ,hypFile, RefFile, out_File])
        perl_script.wait()
        print '\n'
