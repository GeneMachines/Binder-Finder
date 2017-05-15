from Bio import SeqIO, Seq
h = "/Users/j.parker/working_dir/binder_filter/vhh/vhhs-imgt.fasta"
out = "./vhhs-translated.fa"

# filter for sequences whose length is not a multiple of three.
with open(h) as f:
    seqs  = [seq for seq in SeqIO.parse(f, "fasta") \
             if (len(seq) % 3 == 0)]

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

print ("there are {} sequences to be written".format(len(translated)))

SeqIO.write(translated, out, "fasta")
