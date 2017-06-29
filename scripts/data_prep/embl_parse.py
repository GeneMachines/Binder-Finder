#!/usr/bin/python                                                                                                        

from Bio import SeqIO, Seq
import argparse

def opts():
    usage = "embl_parse.py [options] <input annotations>\n"
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument("annot_file", type=str,
                        help="The input annotation file in embl format")
    parser.add_argument("--ids", "-i", type=str, default=False,
                       help="A file with one id per line.")
    parser.add_argument("--output", "-o", type=str, default=False,
                       help="Direct the output to a file. Default is stdout")
    parser.add_argument("--verbose", "-v", action="store_true", default=False,
                       help="Gives more detailed output")

    args = parser.parse_args()

    return args


def parse_embl(input_file, ids):
    """
    Parse the embl annotation file and return only the information needed. 
    """
    with open(input_file, "r") as f:
        if ids:
            records = [r for r in SeqIO.parse(input_file, "embl") if r.id in ids]
        else:
            records = SeqIO.parse(input_file, "embl")        

    return records


def parse_ids(ids):
    """
    Takes a file handle with one id per line and returns a list of ids.
    """
    with open(ids, "r") as f:
        ids = [line.strip() for line in f]

    return ids


def main(args):
    ids = parse_ids(args.ids)
    annots = matching_ids(args.annot, ids)

    return annots


if __name__ == '__main__':
    args = opts()
    annots = main(args)

    for a in annots:
        print a.id
        print a
        print "********"
        print "\n"
