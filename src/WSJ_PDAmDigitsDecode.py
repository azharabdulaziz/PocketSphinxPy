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
ExpName = "PDAmDigits"    
#SNR_Level = "White50db"
TotalNoOfFiles = 35
BaseDir = "/Users/Azhar/Desktop/MDC_Experiments/" + ExpName + "/"
TestFileIds = BaseDir + ExpName+"_test.fileids"
BaseWavPath = "/Users/Azhar/Desktop/Exp6_PDAmDIGITs/PDAmDigits/"
AcModel0 ="Clean.ci_cont";
AcModel20 =ExpName+"_20dB.ci_cont";
AcModel15 =ExpName+"_15dB.cd_cont";
AcModel10 =ExpName+"_10dB.cd_cont";
AcModel = [AcModel0, AcModel10, AcModel15, AcModel20]
ModelsDir = BaseDir + ExpName+"_Models/"
LM = ModelsDir + "PDAm.lm.DMP"
Dic = ModelsDir + "PDAm.dic"

# Create a decoder with certain model
currentModel = AcModel[0]
AM = ModelsDir + currentModel
print 'Model is: ' + AM
print "Acoustic Model: " + AM
print "Language Model: " + LM
print "Dictionary: " + Dic
#sys.exit("HHHHHHHHHHHHHHHHHHHHH")
config = Decoder.default_config()
config.set_string('-logfn', '/dev/null')
config.set_string('-hmm', path.join(AM))
config.set_string('-lm', path.join(LM))
config.set_string('-dict', path.join(Dic))
decoder = Decoder(config)

# Start reading Test list
# SNR_Level = ["wav", "wavWhite5db",]

for snr in range(0,55,5):
    print "\n Input SNR: "+ str(snr) +"    AM: "+ AM
    print 'Start Processing ........\n'
    print '**************************************************************************************************'
    print '0%                                               50%                                          100%'
    if snr == 0:
        ExpWavPath = BaseWavPath + "wav/"
        outDir = BaseDir+"Results/Clean/" + currentModel + "/"
        wavext = ".wav"
    else:
        ExpWavPath = BaseWavPath + "wav" + str(snr) + "db/"
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
    #print "Decoding Test Audio Files for " + ExpWavPath + " using AM " + currentModel
    i=0
    k=0
    with open(TestFileIds) as fp:
        FinalResult = {}
        ListOfFinalResults = []
        HypText = []
        for AudioFile_rp in fp:
            decoder.start_utt()
            xx = AudioFile_rp.strip('\n')
            # Remove last white space
            fNameOnly = xx.strip()
    #                 This is only required for an4                
            #fNameOnly = xx[::-1].replace("/", "-", 1)[::-1]
            #fNameOnly = fNameOnly.split('/', 1)[-1]
            AudioFile = ExpWavPath + fNameOnly + wavext
    
            #print ("Decoding File: " +AudioFile)
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
            # Extract UttId from fNameOnly to be written in Hyp file
            UttId = fNameOnly
            UttId = UttId[::-1].replace("/", "-", 1)[::-1]
            UttId = UttId.split('/', 2)[-1]
            #print fNameOnly
            HypText.append(hypothesis.hypstr + " (" + UttId + ")\n") 
            FinalResult = {"Name":fNameOnly, "Hyp": hypothesis.hypstr, "Score": hypothesis.best_score, "Confidence": hypothesis.prob}
            ListOfFinalResults.append(FinalResult)
            #print 'Best hypothesis: ', hypothesis.hypstr, " model score: ", hypothesis.best_score, " confidence: ", hypothesis.prob
            LatticeFile = outLattice + fNameOnly.replace("/",'-')
            #print 'LatticeFile: ' + LatticeFile
            decoder.get_lattice().write(LatticeFile + '.lat')
            decoder.get_lattice().write_htk(LatticeFile + '.htk') 
            i=i+1
            k=k+1
            sys.stdout.write('*')
            progress = 100*i/TotalNoOfFiles
            #sys.stdout.write("Progress: %d%% \r" % (progress) )
            #sys.stdout.write("Input SNR: %d" % (snr) +" AM: "+ AM +" File: " + fNameOnly +" Progress: %d%%   \r" % (progress) )
            sys.stdout.flush()
    # Running perl WER test
    print "\n"
    
    dump.TextWrite(HypText, outDir+currentModel+".txt")
    dump.CSVDictWrite(ListOfFinalResults, outDir+"/All_"+currentModel+".csv")
    hypFile = outDir+currentModel+".txt" 
    RefFile = BaseDir+"Reference.txt"
    out_File = outDir+"WERReslts_"+currentModel+".txt"
    print 'Finish, now Calculating Error Rate, please wait \n'
    perl_script = subprocess.Popen(["perl", "./word_align.pl",'-silent',hypFile, RefFile, out_File])
    perl_script.wait()
    print '\n'
    
