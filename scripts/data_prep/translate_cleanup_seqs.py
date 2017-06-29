#!/usr/bin/python                                                                                                

from Bio import SeqIO, Seq
from sys import argv
import argparse

def opts():
    usage = "translate_cleanup_seqs [options] <input fasta> <output name>\n"
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument("input_file", type=str,
                        help="The input sequence file")
    parser.add_argument("output_name", type=str,
                        help="Name of the output file")
    parser.add_argument("--verbose", "-v", action="store_true", default=False,
                       help="Gives more detailed output")

    args = parser.parse_args()

    return args


def translate_and_clean(input_file, output_name, verbose):
    # filter for sequences whose length is not a multiple of three.
    with open(input_file, "r") as f, open(output_name, "w") as out:
        seqs  = [seq for seq in SeqIO.parse(f, "fasta") \
                     if (len(seq) % 3 == 0)]

        if verbose:
            print ("there are {} sequences to be translated".format(len(seqs)))

        translated = []
        for seq in seqs:
            t = seq.seq.translate()
            # remove trailing stop-codons for downstream analysis
            t = t.strip("*") 
            # filter for internal stop codons
            if "*" not in t:
                seq.seq = t
                translated.append(seq)
            else:
                pass

        if verbose:
            print ("there are {} sequences written".format(len(translated)))

            SeqIO.write(translated, out, "fasta")


def main():
    args = opts()
    translate_and_clean(args.input_file, args.output_name, args.verbose)


if __name__ == '__main__':
    main()
