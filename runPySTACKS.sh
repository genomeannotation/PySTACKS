module load stacks
export PATH=$PATH:/data0/opt/AlignmentSoftware/bwa/bwa-0.7.12/
module load samtools

##execute PySTACKS
python pystacks.py -sp name -d raw_datas.txt -r genome_data.fa -i index_files.txt -s 1 -pm species_pop.txt -np 2
