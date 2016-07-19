#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import sys
import os
import argparse
from src.controller import Controller

def main():
    parser = argparse.ArgumentParser(
    epilog="""
    PySTACKS: Python STACKS pipeline\n
    Latest version at:\n
    https://github.com/genomeannotation/PySTACKS
    """,
    formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('-sp', '--species_name', help='species name | for output files naming structure')
    parser.add_argument('-b', '--batch_id', help='integer value for batch id | default is 1')
    parser.add_argument('-d', '--raw_data', required=True, help='full path to raw read data (fastq) | Use one data.fq file, or .txt file with one data.fq file per line')
    parser.add_argument('-r', '--reference_genome', help='reference genome (fasta)')
    parser.add_argument('-i', '--index_file', required=True, help='full path to raw read index file | use one index.txt index file, or .txt file with one index.txt file per line (with same order as raw_data)')
    parser.add_argument('-s', '--single_end_data', help='set this flag if raw data is SINGLE-END samples')
    parser.add_argument('-p', '--paired_end_data', help='set this flag if raw data is PAIRED-END samples')
    parser.add_argument('-pm', '--population_map', required=True, help='path to population map for all individuals')
    parser.add_argument('-np', '--num_populations', required=True, help='number of separate populations in the population_map')
    args = parser.parse_args()
    controller = Controller()
    controller.execute(args)


if __name__ == '__main__':
    main()
