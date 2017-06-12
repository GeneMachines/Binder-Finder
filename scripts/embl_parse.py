#!/usr/bin/python                                                                                                        

from Bio import SeqIO, Seq
from sys import argv
import argparse

def opts():
    usage = "embl_parse.py [options] <input annotations> <output name>\n"
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument("input_file", type=str,
                        help="The input sequence file")
#    parser.add_argument("output_name", type=str,
#                        help="Name of the output file")
    parser.add_argument("--verbose", "-v", action="store_true", default=False,
                       help="Gives more detailed output")

    args = parser.parse_args()

    return args


def parse_embl(input_file, ids):
    """
    Parse the embl annotation file and return only the information needed. 
    """

    annots = []
    with open(input_file, "r") as f:
        records = (r for r in SeqIO.parse(input_file, "embl") if r.id in ids)

    return records


def parse_ids(ids):
    
    with open(ids, "r") as f:
        ids = [line.strip() for line in f]
    print ids[:10]
    return ids


def matching_ids(annots, ids):
    annots = parse_embl("~/data/databases/annotations/nrpl2-annotations", parse_ids("../text_searches/progesterone_gp_search.ids"))


def main():
    args = opts()
    parse_embl(args.input_file)


if __name__ == '__main__':
    annots = parse_embl("/Users/j.parker/data/databases/annotations/nrpl2-annotations", parse_ids("../text_searches/progesterone_gp_search.ids"))
    for a in annots:
        print a.id
        print a
        print "********"
        print "\n"
