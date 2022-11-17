import subprocess
import re
import argparse

# Download packgaes
class NameException(Exception): pass
subprocess.call("pip3 install pandas",shell=True)
subprocess.call("pip3 install requests",shell= True)

import pandas as pd
import requests

# Please download ID table(.txt) from NCBI Assembly: https://www.ncbi.nlm.nih.gov/assembly/
def loadIDtable(IDtable):
    SpeciesTable = pd.read_csv(IDtable,names=['GeneBnakAssemblyID','GenBankreleaseID','RefSeqAssemblyID','RefSeqreleaseID'],
    sep='\t',header=0,index_col=False)
    return SpeciesTable

if __name__ == "__main__":
    ap = argparse.ArgumentParser("Download genomic data from NCBI by rsync tool")
    ap.add_argument('-i', help="ID table(.txt) filename")
    ap.add_argument('-n', help='output file name')
    ap.add_argument('-t', help='database, if you want to download data from GenBank,please enter GB; Refseq -- Ref')

    opts = ap.parse_args()
    TableName = opts.i
    inputName = opts.n
    DataOrigin = opts.t
    

    SpeciesTable = loadIDtable(TableName)

    if DataOrigin == 'GB':
        TableColumn = 0
    elif DataOrigin == "Ref":
        TableColumn = 2
    else:
        raise NameException("Error: please choose database: GB/Ref!")

    SpeciesAssembly = SpeciesTable[SpeciesTable.columns[TableColumn]]
    
    count = 0
    ContextFilename = inputName + '_'+DataOrigin+'_Context.txt'
    with open(ContextFilename, "w") as f:
        for i in SpeciesAssembly:
            try:
                TestUrl = 'https://ftp.ncbi.nlm.nih.gov/genomes/all/'+ i[0:3] +'/'+ i[4:7] +'/'+ i[7:10] + '/'+ i[10:13] +'/'
                request = requests.get(TestUrl)
                raw_list = re.compile(r'<a.*?>(.*?)</a>').finditer(request.text.strip())

                for j in raw_list:
                    x = j.group(1)
                    if x[0:3] == 'GCF':
                        count = count + 1
                        fnafile = x[:-1] + "_genomic.fna.gz"
                        fnaUrl_https = TestUrl + x + fnafile
                        fnaUrl_rsync = fnaUrl_https.replace("https","rsync")
                        f.write(fnaUrl_rsync)
                        f.write('\n')

                        gbfffile = x[:-1] + "_genomic.gbff.gz"
                        gbffUrl_https = TestUrl + x + gbfffile
                        gbffUrl_rsync = gbffUrl_https.replace("https","rsync")
                        f.write(gbffUrl_rsync)
                        f.write('\n')


            except TypeError as E:
                pass
    print("Finish search from NCBI:",inputName,"\tToal:",count)