
import subprocess
from subprocess import Popen

BaseDir = '/Users/Azhar/Desktop/MDC_Experiments/an4/'
hypFile = BaseDir + 'Results/Clean/an4_Clean.cd_cont_200/an4_Clean.cd_cont_200.txt' 
RefFile = BaseDir+"RefClean.txt"
outFile = 'word_align_test.txt'
perl_script = subprocess.Popen(["perl", "./word_align.pl",'-silent',hypFile, RefFile, outFile])
perl_script.wait()