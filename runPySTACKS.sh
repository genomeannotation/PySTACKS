module load stacks
export PATH=$PATH:/data0/opt/AlignmentSoftware/bwa/bwa-0.7.12/
module load samtools

##execute PySTACKS
python pystacks.py -sp HwnDros -d raw_datas.txt -r /projects/geibLabs/OutsideProjects/HawaiianDrosophila/Dhet_ddRAD/ReferenceGenome/DHET_01v.201501.genome.fa -i index_files.txt -s 1 -pm All_HwnDros_one_pop.txt -np 2
