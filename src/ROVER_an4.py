'''
Created on Feb 3, 2018

@author: Azhar
'''
ExpName = "an4"
BaseDir = "/Users/Azhar/Desktop/MDC_Experiments/an4/Results/"

Model0 = "an4_Clean.cd_cont_200/"
Model1 = ""
Model2 = ""
Model3 = ""
Models = [Model0,Model1,Model2,Model3]


inputSNR = 5  ## LOOP
currentModel = Models[0] #### Take four

Aligned = BaseDir+"Noisy_"+str(inputSNR)+"db/"+ currentModel+"WERReslts_an4_Clean.cd_cont_200.txt"
print("Aligned file: "+ Aligned)
with open(Aligned) as fp:
    for line in fp:
        print line
