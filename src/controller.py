#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import os
import sys
import argparse
import time

class Controller:

    def __init__(self):
        self.demultiplexed_location = "./processed_SE/"
        self.bwa_mem_location = "./BWA_mem_SE_sams/"
        self.ref_map_location = "./genotypes/catalog/"
        self.denovo_map_location = "./genotypes/noref/"
        self.genotype_location = "./genotypes/"
        
    def get_raw_data(self, args):
        returning = []
        fi = open(args.raw_data, 'r')
        for data in fi.readlines():
            returning.append(data.strip())
        return returning

    def get_index_files(self, args):
        returning = []
        fi = open(args.index_file, 'r')
        for data in fi.readlines():
            returning.append(data.strip())
        return returning

    def get_string_of_files(self, prefix, file_type):
        all_files = ""
        all_fqgz_files = os.listdir(prefix[3:])
        for one_file in all_fqgz_files:
            num = 0 - len(file_type)
            if one_file[num:] == file_type:
                all_files += prefix + one_file + " "
        return all_files

    ## Demultiplex raw data
    def demultiplex_data(self, args):
        if args.single_end_data:
            ## Demultiplex SINGLE-END samples. This will result in one .fastq.gz file for each individual in library.
            if args.raw_data[-4:] == '.txt':
                # many .fq samples
                index = self.get_index_files(args)
                data = self.get_raw_data(args)
                self.create_dir(self.demultiplexed_location)
                self.create_dir(self.demultiplexed_location + args.species_name)
                for i, single_data in enumerate(data):
                    command = "process_radtags -f " + single_data + " -i gzfastq -o " + self.demultiplexed_location + args.species_name + "/ -b " + index[i] + " -e nlaIII -r -c -q"
                    print("\n\nPySTACKS: " + command + "\n")
                    os.system(command)
            else: 
                # one .fq sample
                command = "process_radtags -f " + args.raw_data + " -i gzfastq -o " + self.demultiplexed_location + args.species_name + "/ -b " + args.index_file + " -e nlaIII -r -c -q"
                print("\n\nPySTACKS: " + command + "\n")
                os.system(command)
            
        elif args.paired_end_data:
            ## Demultiplex PAIRED-END samples. This will result in two .fastq.gz (R1 and R2) files for each individual in library.
            self.demultiplexed_location = "./processed_PE/"
            self.create_dir(self.demultiplexed_location)
            self.create_dir(self.demultiplexed_location + args.species_name)
            """nothing yet"""#TODO

    ## Index (if needed) reference assembly to prepare for mapping reads.
    def index_reference_genome(self, args):
        """add check to see if indexing is needed"""#TODO
        p = args.reference_genome.split("/")[-1]
        p = p[:-3]
        command = "bwa index -p " + p + " -a is " + args.reference_genome
        print("\n\nPySTACKS: " + command + "\n")
        os.system(command)

    ## Map reads to reference assembly.
    def map_reads_to_reference(self, args):
        p = args.reference_genome.split("/")[-1]
        p = p[:-3]
        all_fqgz_files = os.listdir(self.demultiplexed_location + args.species_name + "/")
        self.create_dir(self.bwa_mem_location)
        for one_file in all_fqgz_files:
            if one_file[-6:] == ".fq.gz":
                command = "bwa mem -t 32 " + p + " " + self.demultiplexed_location + args.species_name + "/" + one_file + " > " + self.bwa_mem_location + one_file[:-6] + ".sam"
                print("\n\nPySTACKS: " + command + "\n")
                os.system(command)

    ## Make stacks and generate SNP catalogs
    def generate_loci_catalog(self, args):
        all_files = self.get_string_of_files("-s " + self.bwa_mem_location, ".sam")
        self.create_dir(self.genotype_location)
        self.create_dir(self.ref_map_location)
        command = "ref_map.pl -S " + all_files + " -o " + self.ref_map_location + " -m 5 -b " + str(args.batch_id if args.batch_id else 1) + " -T 32 -n 1 -O " + args.population_map
        print("\n\nPySTACKS: " + command + "\n")
        os.system(command)    

    ## Make stacks and map denovo
    def map_reads_and_generate_loci_catalog(self, args):
        all_files = self.get_string_of_files("-s " + self.demultiplexed_location + args.species_name + "/", ".fq.gz")
        self.create_dir(self.genotype_location)
        self.create_dir(self.denovo_map_location)
        self.create_dir(self.denovo_map_location + "log/")
        command = "denovo_map.pl " + all_files + " -o " + self.denovo_map_location + " -m 3 -M 3 -n 3 -t -T 32 -S -b " + str(args.batch_id if args.batch_id else 1) + " -O " + args.population_map + " &>>log/denovo_map1.log"
        print("\n\nPySTACKS: " + command + "\n")
        os.system(command)

    ## Call SNPs
    def call_SNPs(self, args):
        command = "populations -b " + str(args.batch_id if args.batch_id else 1) + " -M " + args.population_map + " -P " + self.ref_map_location + " -m 10 -p " + str(int(args.num_populations)-1) + " -r 0.5 -e nlaIII -t 32 -k -f p_value --vcf --plink --genepop --genomic --ordered_export --write_single_snp > population_log.txt"
        print("\n\nPySTACKS: " + command + "\n")
        os.system(command)

    ## Create output directory
    def create_dir(self, dir_name):
        if not os.path.exists(dir_name):
            os.system('mkdir ' + dir_name)

    ## Main execution
    def execute(self, args):

        # start pipeline
        self.demultiplex_data(args)
        if args.reference_genome:
            self.index_reference_genome(args)
            self.map_reads_to_reference(args)
            self.generate_loci_catalog(args)
        else:
            self.map_reads_and_generate_loci_catalog(args)
        self.call_SNPs(args)
