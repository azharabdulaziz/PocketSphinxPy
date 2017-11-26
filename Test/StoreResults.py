import csv

def CSVDictWrite(Hyp,CSVfileName):
    for h in Hyp:
        keys = h.keys()
        with open(CSVfileName, 'w') as myfile:
            wr = csv.DictWriter(myfile,keys)
            wr.writeheader()
            wr.writerows(Hyp)


def TextWrite(HypList, FileName):
    with open(FileName, mode = 'wt' ) as myfile:
        for i in HypList:
            myfile.write(i)
    
       
            