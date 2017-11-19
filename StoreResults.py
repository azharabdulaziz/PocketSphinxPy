import csv

def CSVDictWrite(Hyp,CSVfileName):
# No need to give the file extension, this function will handle it.
    for h in Hyp:
        keys = h.keys()
        with open(CSVfileName+'.csv', 'w') as myfile:
            wr = csv.DictWriter(myfile,keys)
            wr.writeheader()
            wr.writerows(Hyp)

def TextWrite(HypList, FileName):
    with open(FileName+".txt", mode = 'wt' ) as myfile:
        for i in HypList:
            myfile.write(i)
            