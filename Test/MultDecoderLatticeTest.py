#!/usr/bin/python2.7
# import StoreResults as dump
from os import environ, path
from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *



#AudioFile = "/Users/Azhar/Desktop/Exp2/an4/wav/an4test_clstk/menk/an422-menk-b.sph"
AudioFileName = "fcaw/an406-fcaw-b.sph" 
# Define parameters
ExpName = "an4"    
#SNR_Level = "White50db"
SNR_Level = ""
BaseDir = "/Users/Azhar/Desktop/MDC_Experiments/" + ExpName + "/"
TestFileIds = BaseDir + "an4_test.fileids"
BaseWavPath = "/Users/Azhar/Desktop/Exp2/an4/wav" + SNR_Level + "/an4test_clstk/"
ModelsPath = BaseDir + "an4/AN4_AM/";
AcModel0 ="an4_Clean.cd_cont_200";
AcModel20 ="an4_White20dB.cd_cont_200";
AcModel15 ="an4_White15dB.cd_cont_200";
AcModel10 ="an4_White10dB.cd_cont_200";
AcModel = [AcModel0, AcModel20,AcModel15,AcModel10]
TotalNoOfFiles = 130
# Create a decoder with certain model
AM = BaseDir+"AN4_AM/"+AcModel[0]
LM = BaseDir + "an4.lm"
Dic = BaseDir + "an4.dic"
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
#with open(TestFileIds) as fp:
FinalResult = {}
ListOfFinalResults = []
HypText = []
#   for AudioFile_rp in fp:
#         decoder.start_utt()
xx = AudioFileName.strip('\n')
fNameOnly=xx[::-1].replace("/","-",1)[::-1]
fNameOnly = fNameOnly.split('/',1)[-1]

AudioFile = BaseWavPath + AudioFileName
print ("Decoding File: " +AudioFile)
print ("File Name Only: " + fNameOnly)
stream = open(AudioFile, 'rb')
decoder.start_utt()
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
print 'Best hypothesis: ', hypothesis.hypstr, " model score: ", hypothesis.best_score, " confidence: ", hypothesis.prob
lattice = decoder.get_lattice()




        #decoder.get_lattice().write('goforward.lat')
        #decoder.get_lattice().write_htk('goforward.htk')
       
# print "\n Finish Decoding Test Files."
# dump.TextWrite(HypText, "Hyp.txt")
# dump.CSVDictWrite(ListOfFinalResults, "CSVTest.csv")
# print "Finished ........."
