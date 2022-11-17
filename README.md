# NCBI_Genome_Data_Download

该脚本便于从 NCBI 上批量下载基因组数据，由于大家需求不同，该脚本只是下载了每一个物种基因组中的核酸序列(.fna)以及基因组注释信息(.gbff)，需要下载其他文件可自行修改脚本。

## 用法/示例
```bash
bash download.sh $1 $2 $3
#$1：IDtable.txt
#$2: Output file folder name
#$3: Database (GenBank--GB, Refseq--Ref)
```
