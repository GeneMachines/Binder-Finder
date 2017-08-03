import re
from Bio import SeqIO


def pop_seq_table(dbsession, fasta_file):
    """
    Populates the sql database seq table with embl ids and sequences.
    """
    for rec in SeqIO.parse(fasta_file, "fasta"): # for each sequence in the fasta...
        m = re.search("PN:US(\d+)", rec.description)

        if m:
            patid = m.group(1)
            emblid = rec.id.split(":")[1].split("|")[0] # ...extract the embl id
            seq = str(rec.seq)

            try:
                sequence = Sequence(emblID=emblid, patID=patid, seq=seq)
                dbsession.add(sequence)
            except:
                print(sys.exc_info()[0])
        else:
            pass
    
